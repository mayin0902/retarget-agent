"""YAML run configuration with stable hashing."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

from .hashing import sha256_json

STANDARD_METHODS = ("direct_warp", "crop", "seam", "mesh")


class AnalysisConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    gradient_weight: float = Field(default=0.45, ge=0.0)
    contrast_weight: float = Field(default=0.35, ge=0.0)
    center_weight: float = Field(default=0.20, ge=0.0)
    region_padding_ratio: float = Field(default=0.02, ge=0.0, le=0.25)
    detector_mode: Literal["disabled", "optional", "required"] = "disabled"
    model_root: str = "models/analyzers"
    face_confidence_threshold: float = Field(default=0.55, ge=0.0, le=1.0)
    object_confidence_threshold: float = Field(default=0.35, ge=0.0, le=1.0)
    object_nms_threshold: float = Field(default=0.50, ge=0.0, le=1.0)
    text_binary_threshold: float = Field(default=0.30, ge=0.0, le=1.0)
    text_polygon_threshold: float = Field(default=0.50, ge=0.0, le=1.0)
    text_max_candidates: int = Field(default=200, ge=1, le=1000)
    logo_candidate_limit: int = Field(default=24, ge=0, le=100)


class SelectorConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    selector_id: Literal["technical_risk_v1"] = "technical_risk_v1"


class RunConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: str = "1.0"
    dataset_root: str
    output_root: str = "runs"
    run_id: str
    seed: int = 20260810
    device: Literal["cpu"] = "cpu"
    methods: tuple[str, ...] = STANDARD_METHODS
    analysis: AnalysisConfig = Field(default_factory=AnalysisConfig)
    method_parameters: dict[str, dict[str, Any]] = Field(default_factory=dict)
    selector: SelectorConfig = Field(default_factory=SelectorConfig)

    @model_validator(mode="after")
    def standard_four_exactly_once(self) -> RunConfig:
        if len(self.methods) != 4 or set(self.methods) != set(STANDARD_METHODS):
            raise ValueError(
                f"standard run must contain each method exactly once: {STANDARD_METHODS}"
            )
        unknown = set(self.method_parameters) - set(STANDARD_METHODS)
        if unknown:
            raise ValueError(f"method_parameters contains unknown methods: {sorted(unknown)}")
        return self

    @property
    def config_hash(self) -> str:
        return sha256_json(self.model_dump(mode="json"))


def load_run_config(path: Path) -> RunConfig:
    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    if not isinstance(raw, dict):
        raise ValueError("run config must be a YAML mapping")
    return RunConfig.model_validate(raw)
