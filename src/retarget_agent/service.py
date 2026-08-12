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

    def evaluate(
        self,
        run_dir: Path,
        evaluation_id: str,
        *,
        rerun_detectors: bool = True,
    ) -> dict[str, Any]:
        from .evaluation import EvaluationConfig, evaluate_run

        config = EvaluationConfig(rerun_detectors=rerun_detectors)
        return evaluate_run(run_dir, evaluation_id, config).model_dump(mode="json")

    def replay_agent(
        self,
        run_dir: Path,
        evaluation_id: str,
        agent_run_id: str,
        *,
        mode: str,
        backend_url: str | None = None,
        model_version: str | None = None,
        api_key_env: str | None = None,
        allow_external_aigc: bool = False,
        max_agent_calls: int | None = None,
        fixed_method_id: str | None = None,
    ) -> dict[str, Any]:
        from .agents import (
            AgentMode,
            AgentReplayConfig,
            OpenAICompatibleVisionBackend,
            run_agent_replay,
        )
        from .hashing import sha256_json

        parsed_mode = AgentMode(mode)
        backend = None
        if backend_url is not None or model_version is not None:
            if not backend_url or not model_version:
                raise ValueError("backend_url and model_version must be provided together")
            backend = OpenAICompatibleVisionBackend(
                base_url=backend_url,
                model_version=model_version,
                api_key_env=api_key_env,
                cache_path=(
                    run_dir.resolve()
                    / "agent-cache"
                    / f"{sha256_json({'model_version': model_version})}.json"
                ),
            )
        if parsed_mode is not AgentMode.HARD_RANKER and backend is None:
            raise ValueError("conditional and always-on modes require an Agent backend")
        config = AgentReplayConfig(
            mode=parsed_mode,
            allow_external_aigc=allow_external_aigc,
            max_agent_calls=max_agent_calls,
            fixed_method_id=fixed_method_id,
        )
        return run_agent_replay(
            run_dir,
            evaluation_id,
            agent_run_id,
            config,
            backend,
        ).model_dump(mode="json")

    def build_benchmark(
        self,
        run_dir: Path,
        evaluation_id: str,
        benchmark_id: str,
        route_ids: tuple[str, ...] = (),
    ) -> dict[str, Any]:
        from .benchmarking import build_benchmark_report

        return build_benchmark_report(run_dir, evaluation_id, benchmark_id, route_ids)

    def plan_external_generation(
        self,
        run_dir: Path,
        evaluation_id: str,
        generation_plan_id: str,
        agent_run_ids: tuple[str, ...],
        source_audit_path: Path,
        *,
        maximum_paid_calls: int = 12,
    ) -> dict[str, Any]:
        from .generation_planning import plan_external_generation

        return plan_external_generation(
            run_dir,
            evaluation_id,
            generation_plan_id,
            agent_run_ids,
            source_audit_path,
            maximum_paid_calls=maximum_paid_calls,
        )

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
