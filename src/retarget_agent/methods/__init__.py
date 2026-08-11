"""Built-in deterministic candidate methods."""

from __future__ import annotations

from retarget_agent.protocols import CandidateMethod
from retarget_agent.registry import Registry

from .crop import ProtectionCropMethod
from .direct_warp import DirectWarpMethod
from .mesh import ConstrainedMeshMethod
from .seam import ProtectedSeamMethod


def built_in_methods() -> Registry[CandidateMethod]:
    registry: Registry[CandidateMethod] = Registry("method")
    for method in (
        DirectWarpMethod(),
        ProtectionCropMethod(),
        ProtectedSeamMethod(),
        ConstrainedMeshMethod(),
    ):
        registry.register(method.method_id, method)
    return registry


__all__ = [
    "ConstrainedMeshMethod",
    "DirectWarpMethod",
    "ProtectedSeamMethod",
    "ProtectionCropMethod",
    "built_in_methods",
]

