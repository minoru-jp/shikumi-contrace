"""The structure of a contract asset, expressed with Shikumi (specification REG_027).

Shikumi's structure specification is relative to its root and says nothing about
the name of the root, so the package that holds the contracts can have any name.
Only ``ports`` has a fixed name. What the specification covers is topology: the
kinds of the positions. What the modules contain is checked elsewhere.
"""

from __future__ import annotations

import types

from shikumi_contrace._shikumi import (
    LogicalStructureElement,
    PackageTreeStructure,
    Shikumi,
    StructuralKind,
    StructureElement,
    StructureFragment,
    StructureSpecification,
)

__all__ = ["CONTRACT_ASSET_STRUCTURE", "structure_findings"]

PORTS = "ports"

# What is inside a module (classes, functions) is not structure to regulate here.
_MODULE = StructureFragment.unconstrained(StructuralKind.MODULE)
_PACKAGE = StructureFragment.unconstrained(StructuralKind.PACKAGE)
# A class defined in the __init__ of a package is an entity directly below the
# package. Whether a definition belongs there is a question about content, not
# topology, so the structure does not regulate it.
_ENTITY = StructureFragment.unconstrained(StructuralKind.ENTITY)

# ``ports`` is a package, and what it holds directly are modules of any name.
_PORTS = StructureFragment(
    [StructureElement((), StructuralKind.PACKAGE)],
    logical_elements=[
        LogicalStructureElement(
            parent=(), logical_name="shape", fragment=_MODULE, min_count=0
        ),
        LogicalStructureElement(
            parent=(), logical_name="definition", fragment=_ENTITY, min_count=0
        ),
    ],
)

CONTRACT_ASSET_STRUCTURE = StructureSpecification(
    [
        StructureElement((), StructuralKind.PACKAGE),
        # Not every contract asset needs boundary types, so ``ports`` is optional.
        # When it exists, it has to be a package.
        StructureElement((PORTS,), StructuralKind.PACKAGE, required=False),
    ],
    logical_elements=[
        # The contracts: modules and sub-packages, of any name.
        LogicalStructureElement(
            parent=(), logical_name="contract", fragment=_MODULE, min_count=0
        ),
        LogicalStructureElement(
            parent=(), logical_name="group", fragment=_PACKAGE, min_count=0
        ),
        LogicalStructureElement(
            parent=(), logical_name="definition", fragment=_ENTITY, min_count=0
        ),
    ],
    mounts=[_PORTS.at((PORTS,))],
)

_SHIKUMI = Shikumi(structure=PackageTreeStructure())


def _is_below(path: str, prefixes: list[str]) -> bool:
    return any(path.startswith(prefix + ".") for prefix in prefixes)


def structure_findings(package: types.ModuleType) -> list[str]:
    """What does not match CONTRACT_ASSET_STRUCTURE below *package* (REG_027).

    What lies below a position that already mismatches is a consequence of that
    mismatch, so it is left out.
    """
    result = _SHIKUMI.validate(
        package, structure_specification=CONTRACT_ASSET_STRUCTURE
    )
    kept: list[str] = []
    reported: list[str] = []
    for diagnostic in result.diagnostics:
        if not (diagnostic.code or "").startswith("structure."):
            continue
        path: str | None = None
        if diagnostic.subject is not None:
            node = result.view.structure.node_for(diagnostic.subject)
            if node is not None:
                path = ".".join(node.path)
        if path is not None:
            if _is_below(path, reported):
                continue
            reported.append(path)
        kept.append(diagnostic.message)
    return kept
