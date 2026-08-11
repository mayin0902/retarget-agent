"""Deterministic comparison grids for review and smoke diagnostics."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from .models import CandidateRecord, DecisionRecord, TaskSpec


def comparison_grid(
    source: np.ndarray,
    task: TaskSpec,
    candidates: list[CandidateRecord],
    decision: DecisionRecord,
    run_dir: Path,
) -> np.ndarray:
    preview_scale = min(1.0, 640 / max(task.target.width, task.target.height))
    panel_width = max(1, round(task.target.width * preview_scale))
    panel_height = max(1, round(task.target.height * preview_scale))
    label_height = 26
    cell_width = panel_width
    cell_height = panel_height + label_height
    canvas = Image.new("RGB", (cell_width * 3, cell_height * 2), (30, 30, 30))

    source_panel = Image.fromarray(source, mode="RGB").resize(
        (panel_width, panel_height), Image.Resampling.LANCZOS
    )
    panels: list[tuple[str, Image.Image]] = [("source (preview)", source_panel)]
    for candidate in candidates:
        if candidate.output is None:
            panel = Image.new("RGB", (panel_width, panel_height), (90, 25, 25))
            draw = ImageDraw.Draw(panel)
            draw.text((8, 8), candidate.error_summary or "FAILED", fill=(255, 255, 255))
        else:
            with Image.open(run_dir / candidate.output.relative_path) as opened:
                panel = opened.convert("RGB").resize(
                    (panel_width, panel_height), Image.Resampling.LANCZOS
                )
        marker = " TOP-1" if candidate.candidate_id == decision.best_candidate_id else ""
        panels.append(
            (
                f"{candidate.method_id} [{candidate.generation_status.value}]{marker}",
                panel,
            )
        )

    for index, (label, panel) in enumerate(panels[:6]):
        column = index % 3
        row = index // 3
        x = column * cell_width
        y = row * cell_height
        canvas.paste(panel, (x, y + label_height))
        draw = ImageDraw.Draw(canvas)
        draw.text((x + 6, y + 6), label, fill=(245, 245, 245))
    return np.asarray(canvas)
