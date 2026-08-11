"""Command-line adapters. Business logic lives behind RetargetApplicationService."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer

from . import __version__

app = typer.Typer(help="Replayable four-candidate image retargeting experiments.")
dataset_app = typer.Typer(help="Dataset materialization and validation.")
run_app = typer.Typer(help="Generation runs.")
replay_app = typer.Typer(help="Evaluation Replay over frozen candidates.")
review_app = typer.Typer(help="Human review tools.")
app.add_typer(dataset_app, name="dataset")
app.add_typer(run_app, name="run")
app.add_typer(replay_app, name="replay")
app.add_typer(review_app, name="review")


@app.command()
def version() -> None:
    """Print the installed package version."""
    typer.echo(__version__)


@dataset_app.command("validate")
def dataset_validate(
    dataset_root: Annotated[Path, typer.Argument(exists=True, file_okay=False)],
) -> None:
    """Validate a Folder/CSV dataset without generating candidates."""
    from .service import RetargetApplicationService

    result = RetargetApplicationService.default().validate_dataset(dataset_root)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["valid"]:
        raise typer.Exit(code=2)


@run_app.command("generate")
def run_generate(
    config_path: Annotated[Path, typer.Argument(exists=True, dir_okay=False)],
) -> None:
    """Execute one standard four-candidate Generation Run."""
    from .service import RetargetApplicationService

    result = RetargetApplicationService.default().generate_from_config(config_path)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command("report")
def report(
    run_dir: Annotated[Path, typer.Argument(exists=True, file_okay=False)],
) -> None:
    """Rebuild a report from frozen candidate and review records."""
    from .service import RetargetApplicationService

    result = RetargetApplicationService.default().build_report(run_dir)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@app.command("audit")
def audit(
    run_dir: Annotated[Path, typer.Argument(exists=True, file_okay=False)],
) -> None:
    """Audit a frozen run against the standard four-candidate contract."""
    from .audit import audit_run_contract

    result = audit_run_contract(run_dir)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))
    if result["status"] != "PASS":
        raise typer.Exit(code=2)


@replay_app.command("run")
def replay_run(
    run_dir: Annotated[Path, typer.Argument(exists=True, file_okay=False)],
    replay_id: Annotated[str, typer.Option("--replay-id")],
) -> None:
    """Create a new Decision set without changing Candidate artifacts."""
    from .service import RetargetApplicationService

    result = RetargetApplicationService.default().replay(run_dir, replay_id)
    typer.echo(json.dumps(result, ensure_ascii=False, indent=2))


@review_app.command("ui")
def review_ui(
    run_dir: Annotated[Path, typer.Argument(exists=True, file_okay=False)],
) -> None:
    """Launch Streamlit against a frozen run."""
    from .service import RetargetApplicationService

    RetargetApplicationService.default().launch_review_ui(run_dir)


@review_app.command("web")
def review_web(
    run_dir: Annotated[Path, typer.Argument(exists=True, file_okay=False)],
    host: Annotated[str, typer.Option("--host", help="Bind address.")] = "127.0.0.1",
    port: Annotated[
        int,
        typer.Option("--port", min=1, max=65535, help="Local HTTP port."),
    ] = 8765,
) -> None:
    """Launch the FastAPI review website against a frozen run."""
    from .service import RetargetApplicationService

    typer.echo(f"Review website: http://{host}:{port}")
    if host not in {"127.0.0.1", "localhost", "::1"}:
        typer.echo("Warning: non-loopback binding exposes this unauthenticated local review tool.")
    RetargetApplicationService.default().launch_review_web(run_dir, host=host, port=port)
