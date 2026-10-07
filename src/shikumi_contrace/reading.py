"""Read what contracts and tests declare (specification RDG_001-RDG_010).

Independent of any test runner. Information attached under another decorator
(``functools.wraps``, ``mock.patch``...) is found by following ``__wrapped__``
(RDG_007), and information is returned in the order it was written (RDG_009).
"""

from __future__ import annotations

import inspect
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from types import ModuleType

from shikumi_contrace._model import (
    ANNOTATION,
    BINDING,
    DEPENDENCY,
    KIND,
    ON_VIOLATION,
    RELATION,
    SUBJECT,
    AnnotationValue,
    Binding,
    Relation,
    Word,
    enclosing_class,
    infos_on,
    iter_tests,
    namespace_of,
    ordered_infos,
)

__all__ = [
    "Annotation",
    "Binding",
    "Clause",
    "Relation",
    "annotations_of",
    "bindings_of",
    "clauses_of",
    "dependencies_of",
    "dependents_of",
    "relations_of",
    "tests_of",
    "untested_clauses",
]


@dataclass(frozen=True)
class Annotation:
    """An annotation: a word and an optional text."""

    word: Word
    text: str | None


@dataclass(frozen=True)
class Clause:
    """A clause of a contract."""

    cls: type
    kind: Word
    on_violation: Word | None
    statement: str
    annotations: tuple[Annotation, ...]
    path: str


def _is_decorator_form(value: AnnotationValue) -> bool:
    return value.form == "decorator"


def relations_of(test: object) -> tuple[Relation, ...]:
    """The relations a test declares (RDG_002)."""
    return ordered_infos(test, RELATION)


def dependencies_of(contract: type) -> tuple[type, ...]:
    """The contracts that *contract* directly depends on, in written order."""
    return infos_on(contract, DEPENDENCY)


def _classes_within(item: object) -> Iterator[type]:
    roots: Iterable[type]
    if isinstance(item, ModuleType):
        roots = (
            value
            for value in namespace_of(item).values()
            if isinstance(value, type) and value.__module__ == item.__name__
        )
    elif isinstance(item, type):
        roots = (item,)
    else:
        roots = ()

    stack = list(reversed(tuple(roots)))
    while stack:
        cls = stack.pop()
        yield cls
        nested = [
            value
            for name, value in namespace_of(cls).items()
            if isinstance(value, type) and _is_nested(value, cls, name)
        ]
        stack.extend(reversed(nested))


def dependents_of(contract: type, within: Iterable[object] = ()) -> tuple[type, ...]:
    """Contracts in *within* that directly depend on *contract*."""
    found: list[type] = []
    seen: set[int] = set()
    for item in within:
        for candidate in _classes_within(item):
            if id(candidate) in seen:
                continue
            seen.add(id(candidate))
            if infos_on(candidate, SUBJECT) and contract in dependencies_of(candidate):
                found.append(candidate)
    return tuple(found)


def annotations_of(obj: object) -> tuple[Annotation, ...]:
    """The annotations declared on a contract, member, clause or test (RDG_002)."""
    return tuple(
        Annotation(value.word, value.text)
        for value in ordered_infos(obj, ANNOTATION, _is_decorator_form)
    )


def bindings_of(obj: object) -> tuple[Binding, ...]:
    """The bindings declared on *obj*.

    For a test function or method, the bindings of the class it is defined in
    are included (SYN_018, RDG_002).
    """
    found = list(ordered_infos(obj, BINDING))
    if not isinstance(obj, type):
        owner = enclosing_class(obj)
        if owner is not None:
            found.extend(ordered_infos(owner, BINDING))
    return tuple(found)


def _is_nested(value: type, owner: type, name: str) -> bool:
    return (
        value.__module__ == owner.__module__
        and value.__qualname__ == f"{owner.__qualname__}.{name}"
    )


def _clause(cls: type, kind: Word, root: type) -> Clause:
    violation_behaviors = infos_on(cls, ON_VIOLATION)
    return Clause(
        cls=cls,
        kind=kind,
        on_violation=violation_behaviors[0] if violation_behaviors else None,
        statement=inspect.getdoc(cls) or "",
        annotations=annotations_of(cls),
        path=cls.__qualname__.removeprefix(f"{root.__qualname__}."),
    )


def clauses_of(contract: type) -> tuple[Clause, ...]:
    """The clauses of a contract, in definition order (RDG_003)."""
    found: list[Clause] = []

    def walk(owner: type) -> None:
        for name, value in namespace_of(owner).items():
            if isinstance(value, type) and _is_nested(value, owner, name):
                kinds = infos_on(value, KIND)
                if kinds:
                    found.append(_clause(value, kinds[0], contract))
                walk(value)

    walk(contract)
    return tuple(found)


def tests_of(
    clause: Clause | type, within: Iterable[object] = ()
) -> tuple[object, ...]:
    """The tests related to *clause*, looked up in *within* (RDG_004).

    *within* holds the modules (or classes, or functions) to search.
    """
    target = clause.cls if isinstance(clause, Clause) else clause
    return tuple(
        test
        for test in iter_tests(within)
        if any(relation.clause is target for relation in relations_of(test))
    )


def untested_clauses(
    contract: type, within: Iterable[object] = ()
) -> tuple[Clause, ...]:
    """The clauses of *contract* that no test in *within* relates to (RDG_005).

    This is a traceability query only. It does not infer whether a clause ought
    to have a test from its kind, violation behavior, or any other meaning.
    """
    scope = tuple(within)
    return tuple(c for c in clauses_of(contract) if not tests_of(c, scope))


# `tests_of` starts with "test", so pytest would collect it as a test when it is
# imported into a test module. Say explicitly that it is not a test.
setattr(tests_of, "__test__", False)  # noqa: B010
