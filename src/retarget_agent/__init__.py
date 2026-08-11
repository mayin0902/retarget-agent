"""retarget-agent public package."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("retarget-agent")
except PackageNotFoundError:  # pragma: no cover - editable source without metadata
    __version__ = "0.1.0"

__all__ = ["__version__"]

