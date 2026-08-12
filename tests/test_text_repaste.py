from __future__ import annotations

import cv2
import numpy as np

from retarget_agent.models import Rect, RegionKind, RegionRecord
from retarget_agent.text_repaste import TextRepasteConfig, repaste_text_layers


def _text_region(**attributes: object) -> RegionRecord:
    values = {
        "semantic_type": "text",
        "recognized_text": "SALE 50",
        "recognition_confidence": 0.9,
    }
    values.update(attributes)
    return RegionRecord(
        region_id="text-1",
        kind=RegionKind.MUST_KEEP,
        rect=Rect(x1=20, y1=30, x2=100, y2=60),
        importance=1.0,
        tolerance=0.0,
        confidence=0.95,
        source="fixture-ocr",
        label="text",
        attributes=values,
    )


def test_repaste_preserves_dimensions_and_changes_only_text_area() -> None:
    source = np.full((100, 120, 3), 245, np.uint8)
    cv2.putText(source, "SALE", (22, 52), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (5, 5, 5), 2)
    generated = np.full((200, 200, 3), (80, 130, 180), np.uint8)

    result, metrics = repaste_text_layers(source, generated, (_text_region(),))

    assert result.shape == generated.shape
    assert not np.array_equal(result, generated)
    assert metrics.eligible_region_count == metrics.pasted_region_count == 1
    assert 0 < metrics.pasted_pixel_fraction < 0.25
    assert np.array_equal(result[:40], generated[:40])


def test_low_confidence_text_is_not_repasted() -> None:
    source = np.full((100, 120, 3), 255, np.uint8)
    generated = np.zeros((200, 200, 3), np.uint8)
    region = _text_region(recognition_confidence=0.1)

    result, metrics = repaste_text_layers(source, generated, (region,))

    assert np.array_equal(result, generated)
    assert metrics.eligible_region_count == 0
    assert metrics.warnings == ("no_eligible_text_regions",)


def test_invalid_image_contract_is_rejected() -> None:
    source = np.zeros((10, 10), np.uint8)
    generated = np.zeros((10, 10, 3), np.uint8)
    try:
        repaste_text_layers(source, generated, (), TextRepasteConfig())
    except ValueError as error:
        assert "uint8 RGB" in str(error)
    else:
        raise AssertionError("invalid source image should fail")


def test_opaque_patch_replaces_existing_generated_text_without_touching_other_regions() -> None:
    source = np.full((100, 120, 3), 245, np.uint8)
    cv2.putText(source, "SALE", (22, 52), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (5, 5, 5), 2)
    generated = np.full((200, 200, 3), (80, 130, 180), np.uint8)
    cv2.putText(generated, "BAD", (36, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)

    result, metrics = repaste_text_layers(
        source,
        generated,
        (_text_region(),),
        TextRepasteConfig(composite_mode="opaque_patch", patch_feather_radius=4),
    )

    assert metrics.pasted_region_count == 1
    assert np.array_equal(result[:55], generated[:55])
    assert np.array_equal(result[125:], generated[125:])
    assert not np.array_equal(result[60:120], generated[60:120])
