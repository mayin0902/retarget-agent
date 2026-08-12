"""Deterministic exact-pixel text repaste for generated square backgrounds."""

from __future__ import annotations

import time
from typing import Literal

import cv2
import numpy as np
from pydantic import BaseModel, ConfigDict, Field

from .models import RegionRecord


class TextRepasteConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    minimum_detection_confidence: float = Field(default=0.45, ge=0.0, le=1.0)
    minimum_recognition_confidence: float = Field(default=0.25, ge=0.0, le=1.0)
    maximum_regions: int = Field(default=40, ge=1, le=200)
    contrast_threshold: float = Field(default=16.0, ge=1.0, le=128.0)
    feather_radius: int = Field(default=2, ge=0, le=16)
    minimum_mask_fraction: float = Field(default=0.01, ge=0.0, le=1.0)
    composite_mode: Literal["foreground_alpha", "opaque_patch"] = "foreground_alpha"
    patch_feather_radius: int = Field(default=8, ge=0, le=64)


class TextRepasteMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    source_region_count: int = Field(ge=0)
    eligible_region_count: int = Field(ge=0)
    pasted_region_count: int = Field(ge=0)
    pasted_pixel_fraction: float = Field(ge=0.0, le=1.0)
    wall_seconds: float = Field(ge=0.0)
    cpu_seconds: float = Field(ge=0.0)
    warnings: tuple[str, ...] = ()


def _is_text_region(region: RegionRecord, config: TextRepasteConfig) -> bool:
    semantic_type = str(region.attributes.get("semantic_type", ""))
    recognition_confidence = float(region.attributes.get("recognition_confidence", 0.0))
    return (
        semantic_type == "text"
        and region.confidence >= config.minimum_detection_confidence
        and recognition_confidence >= config.minimum_recognition_confidence
    )


def _foreground_alpha(patch: np.ndarray, config: TextRepasteConfig) -> np.ndarray:
    gray = cv2.cvtColor(patch, cv2.COLOR_RGB2GRAY)
    border = np.concatenate((gray[0], gray[-1], gray[:, 0], gray[:, -1]))
    background = float(np.median(border))
    contrast = np.abs(gray.astype(np.float32) - background)
    edges = cv2.Canny(gray, 60, 160)
    radius = max(1, round(min(gray.shape) * 0.025))
    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (radius * 2 + 1, radius * 2 + 1),
    )
    edge_mask = cv2.dilate(edges, kernel)
    mask = np.where(
        (contrast >= config.contrast_threshold) | (edge_mask > 0),
        255,
        0,
    ).astype(np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    if config.feather_radius:
        size = config.feather_radius * 2 + 1
        mask = cv2.GaussianBlur(mask, (size, size), 0)
    return mask.astype(np.float32) / 255.0


def _opaque_patch_alpha(patch: np.ndarray, config: TextRepasteConfig) -> np.ndarray:
    """Return an opaque interior with a soft edge for exact source-patch restoration."""

    height, width = patch.shape[:2]
    radius = min(config.patch_feather_radius, max(0, (min(height, width) - 1) // 2))
    if radius == 0:
        return np.ones((height, width), dtype=np.float32)
    axis_y = np.minimum(np.arange(height), np.arange(height)[::-1])
    axis_x = np.minimum(np.arange(width), np.arange(width)[::-1])
    edge_distance = np.minimum(axis_y[:, None], axis_x[None, :]).astype(np.float32)
    return np.clip(edge_distance / radius, 0.0, 1.0)


def repaste_text_layers(
    source_rgb: np.ndarray,
    generated_rgb: np.ndarray,
    regions: tuple[RegionRecord, ...],
    config: TextRepasteConfig | None = None,
) -> tuple[np.ndarray, TextRepasteMetrics]:
    """Repaste detected source-text pixels at normalized positions on a generated base."""

    config = config or TextRepasteConfig()
    if (
        source_rgb.ndim != 3
        or generated_rgb.ndim != 3
        or source_rgb.shape[2] != 3
        or generated_rgb.shape[2] != 3
        or source_rgb.dtype != np.uint8
        or generated_rgb.dtype != np.uint8
    ):
        raise ValueError("source and generated images must be uint8 RGB arrays")
    started_wall = time.perf_counter()
    started_cpu = time.process_time()
    source_height, source_width = source_rgb.shape[:2]
    target_height, target_width = generated_rgb.shape[:2]
    eligible = sorted(
        (region for region in regions if _is_text_region(region, config)),
        key=lambda item: (-item.importance, -item.confidence, item.region_id),
    )[: config.maximum_regions]
    result = generated_rgb.copy()
    pasted = 0
    pasted_mask = np.zeros((target_height, target_width), dtype=np.uint8)
    for region in eligible:
        source_rect = region.rect
        x1 = min(source_width, source_rect.x1)
        y1 = min(source_height, source_rect.y1)
        x2 = min(source_width, source_rect.x2)
        y2 = min(source_height, source_rect.y2)
        if x2 <= x1 or y2 <= y1:
            continue
        target_x1 = max(0, min(target_width - 1, round(x1 / source_width * target_width)))
        target_y1 = max(0, min(target_height - 1, round(y1 / source_height * target_height)))
        target_x2 = max(
            target_x1 + 1,
            min(target_width, round(x2 / source_width * target_width)),
        )
        target_y2 = max(
            target_y1 + 1,
            min(target_height, round(y2 / source_height * target_height)),
        )
        patch = source_rgb[y1:y2, x1:x2]
        width = target_x2 - target_x1
        height = target_y2 - target_y1
        interpolation = (
            cv2.INTER_AREA
            if width <= patch.shape[1] and height <= patch.shape[0]
            else cv2.INTER_LANCZOS4
        )
        resized = cv2.resize(patch, (width, height), interpolation=interpolation)
        alpha = (
            _foreground_alpha(resized, config)
            if config.composite_mode == "foreground_alpha"
            else _opaque_patch_alpha(resized, config)
        )
        if float(np.mean(alpha > 0.05)) < config.minimum_mask_fraction:
            continue
        destination = result[target_y1:target_y2, target_x1:target_x2].astype(np.float32)
        blended = resized.astype(np.float32) * alpha[..., None] + destination * (
            1.0 - alpha[..., None]
        )
        result[target_y1:target_y2, target_x1:target_x2] = np.clip(blended, 0, 255).astype(np.uint8)
        pasted_mask[target_y1:target_y2, target_x1:target_x2] = np.maximum(
            pasted_mask[target_y1:target_y2, target_x1:target_x2],
            (alpha * 255).astype(np.uint8),
        )
        pasted += 1
    warnings: list[str] = []
    if not eligible:
        warnings.append("no_eligible_text_regions")
    elif not pasted:
        warnings.append("eligible_text_masks_empty")
    metrics = TextRepasteMetrics(
        source_region_count=len(regions),
        eligible_region_count=len(eligible),
        pasted_region_count=pasted,
        pasted_pixel_fraction=float(np.mean(pasted_mask > 0)),
        wall_seconds=time.perf_counter() - started_wall,
        cpu_seconds=time.process_time() - started_cpu,
        warnings=tuple(warnings),
    )
    return result, metrics
