"""shikumi-contrace - describe the contract of a type as a standalone asset.

This is the top level: the names for *writing* contracts and tests. Reading and
checking live in :mod:`shikumi_contrace.reading` and :mod:`shikumi_contrace.checking`; the optional
pytest integration is :mod:`shikumi_contrace.pytest`.
"""

from metamk import Mk as Phase
from metamk import phase_of

from shikumi_contrace._descriptors import binds
from shikumi_contrace._vocabulary import (
    INV,
    OUT_OF_SCOPE,
    POST,
    PRE,
    REJECTED,
    assumption,
    boundary,
    caution,
    concurrency,
    critical,
    define,
    depends_on,
    deprecated,
    example,
    kind,
    legacy,
    manual,
    member,
    note,
    on_violation,
    performance,
    provisional,
    rationale,
    regression,
    security,
    source,
    subject,
    todo,
    upholds,
    violates,
)

# Everything below is re-exported explicitly through ``__all__`` (SYN_023):
#   descriptors (written as ``name @= value`` in a class body):
#       subject, member, kind, depends_on, on_violation
#   clause kinds: PRE, POST, INV
#   precondition violation behavior: OUT_OF_SCOPE, REJECTED
#   relation words: upholds, violates
#   annotation words: note, rationale, caution, example, source, assumption,
#       security, performance, concurrency, critical, todo, provisional, legacy,
#       deprecated, manual, boundary, regression
#   binding and custom words: binds, define
#   metamk, re-exported (AIM_014): Phase (alias of Mk), phase_of
__all__ = [
    "INV",
    "OUT_OF_SCOPE",
    "POST",
    "PRE",
    "REJECTED",
    "Phase",
    "assumption",
    "binds",
    "boundary",
    "caution",
    "concurrency",
    "critical",
    "define",
    "depends_on",
    "deprecated",
    "example",
    "kind",
    "legacy",
    "manual",
    "member",
    "note",
    "on_violation",
    "performance",
    "phase_of",
    "provisional",
    "rationale",
    "regression",
    "security",
    "source",
    "subject",
    "todo",
    "upholds",
    "violates",
]
