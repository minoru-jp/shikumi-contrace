"""The single place that imports Shikumi's public API (specification REG_018).

The rest of shikumi-contrace reaches Shikumi only through the names re-exported here.
"""

from __future__ import annotations

from shikumi import (
    Cardinality,
    ClassBinding,
    InformationType,
    LogicalStructureElement,
    Shikumi,
    StructuralKind,
    StructureElement,
    StructureFragment,
    StructureSpecification,
    attach_information,
    class_binding,
    information_of,
    record_descriptor_use,
)
from shikumi.standard import PackageTreeStructure

__all__ = [
    "Cardinality",
    "ClassBinding",
    "InformationType",
    "LogicalStructureElement",
    "PackageTreeStructure",
    "Shikumi",
    "StructuralKind",
    "StructureElement",
    "StructureFragment",
    "StructureSpecification",
    "attach_information",
    "class_binding",
    "information_of",
    "record_descriptor_use",
]
