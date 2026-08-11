"""One application surface shared by CLI, Streamlit and FastAPI."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class RetargetApplicationService:
    """M0-M4 use cases; concrete collaborators are assembled by ``default``."""

    @classmethod
    def default(cls) -> RetargetApplicationService:
        return cls()

    def validate_dataset(self, dataset_root: Path) -> dict[str, Any]:
        from .datasets import FolderCsvDatasetAdapter

        result = FolderCsvDatasetAdapter().validate(dataset_root)
        return {
            "valid": result.valid,
            "dataset_id": result.dataset_id,
            "dataset_fingerprint": result.dataset_fingerprint,
            "task_count": len(result.tasks),
            "errors": result.errors,
            "warnings": result.warnings,
        }

    def generate_from_config(self, config_path: Path) -> dict[str, Any]:
        from .config import load_run_config
        from .runner import GenerationRunner

        manifest = GenerationRunner.default().run(load_run_config(config_path), config_path)
        return manifest.model_dump(mode="json")

    def build_report(self, run_dir: Path) -> dict[str, Any]:
        from .reporting import build_run_report

        return build_run_report(run_dir)

    def replay(self, run_dir: Path, replay_id: str) -> dict[str, Any]:
        from .replay import run_evaluation_replay

        return run_evaluation_replay(run_dir, replay_id).model_dump(mode="json")

    def load_review_workspace(self, run_dir: Path, reviewer_id: str) -> dict[str, Any]:
        from .review import load_review_workspace

        return load_review_workspace(run_dir, reviewer_id)

    def save_task_reviews(
        self,
        run_dir: Path,
        reviewer_id: str,
        task_id: str,
        reviews: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        from .review import save_task_reviews

        return save_task_reviews(run_dir, reviewer_id, task_id, reviews)

    def launch_review_ui(self, run_dir: Path) -> None:
        import subprocess
        import sys

        app_path = Path(__file__).with_name("streamlit_app.py")
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", str(app_path), "--", str(run_dir)],
            check=True,
        )

    def launch_review_web(
        self,
        run_dir: Path,
        *,
        host: str = "127.0.0.1",
        port: int = 8765,
    ) -> None:
        """Run the local review web adapter against one frozen Generation Run."""
        import uvicorn

        from .web_app import create_review_app

        run_dir = run_dir.resolve()
        if not (run_dir / "run.json").is_file():
            raise ValueError(f"not a Generation Run directory: {run_dir}")
        uvicorn.run(
            create_review_app(run_dir, service=self),
            host=host,
            port=port,
            log_level="info",
        )
