"""Internal model: words, information types and helpers to attach and read information.

Dynamic Python (``getattr``, ``vars``, ``typing.get_args``) and Shikumi's
``information_of`` return ``Any``. Every use of them is wrapped here in a small
function with a declared return type, so that ``Any`` does not spread into the
rest of shikumi-contrace.
"""

from __future__ import annotations

import inspect
import sys
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from types import ModuleType
from typing import Literal, TypeVar, get_args, get_origin

from shikumi_contrace._shikumi import (
    Cardinality,
    InformationType,
    attach_information,
    information_of,
    record_descriptor_use,
)

T = TypeVar("T")

WordCategory = Literal["kind", "violation", "relation", "annotation"]
Form = Literal["decorator", "body"]


@dataclass(frozen=True)
class Word:
    """A word of the vocabulary. Standard and custom words are values of this type."""

    name: str
    category: WordCategory


@dataclass(frozen=True)
class Relation:
    """A test's relation to a clause: a relation word and the clause class."""

    word: Word
    clause: type


@dataclass(frozen=True)
class Binding:
    """A binding of a subject type to an implementation."""

    subject: type
    implementation: object


@dataclass(frozen=True)
class AnnotationValue:
    """What is stored for an annotation. ``form`` lets reading restore the written order."""

    word: Word
    text: str | None
    form: Form


# The information types shikumi-contrace recognizes. Vocabulary is made of *values*,
# so custom words need no registration (VOC_008).
SUBJECT: InformationType[type] = InformationType("subject", type)
MEMBER: InformationType[object] = InformationType("member", object)
KIND: InformationType[Word] = InformationType("kind", Word)
RELATION: InformationType[Relation] = InformationType(
    "relation", Relation, Cardinality.MANY
)
ANNOTATION: InformationType[AnnotationValue] = InformationType(
    "annotation", AnnotationValue, Cardinality.MANY
)
BINDING: InformationType[Binding] = InformationType(
    "binding", Binding, Cardinality.MANY
)
DEPENDENCY: InformationType[type] = InformationType(
    "dependency", type, Cardinality.MANY
)
ON_VIOLATION: InformationType[Word] = InformationType("on_violation", Word)


# --- the places where Any is absorbed -----------------------------------------


def attr_of(obj: object, name: str) -> object | None:
    """``getattr(obj, name, None)`` with a declared type."""
    return getattr(obj, name, None)


def namespace_of(obj: object) -> dict[str, object]:
    """``vars(obj)`` with a declared type."""
    return vars(obj)


def type_args(alias: object) -> tuple[object, ...]:
    """``typing.get_args(alias)`` with a declared type."""
    return get_args(alias)


def origin_of(alias: object) -> object | None:
    """``typing.get_origin(alias)`` with a declared type."""
    return get_origin(alias)


# --- attaching and reading information ----------------------------------------


def attach(obj: object, information_type: InformationType[T], value: T) -> None:
    _ = attach_information(obj, information_type, value)


def record_use(owner: object, descriptor: object) -> None:
    _ = record_descriptor_use(owner, descriptor)


def infos_on(obj: object, information_type: InformationType[T]) -> tuple[T, ...]:
    """Information of one type attached to exactly *obj* (no unwrapping)."""
    # Shikumi's information_of returns `Information[Any]`: a subject can carry
    # information of several types. This is the one place where that Any is met.
    return tuple(
        record.value  # pyright: ignore[reportAny]
        for record in information_of(obj)
        if record.type is information_type
    )


def wrapped_chain(obj: object) -> Iterator[object]:
    """Yield *obj* and the objects it wraps (``__wrapped__``, ``__func__``)."""
    seen: set[int] = set()
    current: object | None = obj
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        yield current
        wrapped = attr_of(current, "__wrapped__")
        current = wrapped if wrapped is not None else attr_of(current, "__func__")


def ordered_infos(
    obj: object,
    information_type: InformationType[T],
    is_decorator: Callable[[T], bool] = lambda _value: True,
) -> tuple[T, ...]:
    """Information on *obj* and on everything it wraps, in the order it was written.

    Decorators are applied from the bottom up, so the information they attach
    is reversed to read top to bottom. For a class, the decorators come first
    (they are written above it), then the ``@=`` statements of its body, in
    order. Information of an outer wrapper comes before that of the function it
    wraps (RDG_007, RDG_009).
    """
    collected: list[T] = []
    for item in wrapped_chain(obj):
        values = infos_on(item, information_type)
        collected.extend(reversed([v for v in values if is_decorator(v)]))
        collected.extend(v for v in values if not is_decorator(v))
    return tuple(collected)


# --- finding classes and tests -------------------------------------------------


def _class_at(module_name: object, parts: list[str]) -> type | None:
    module = sys.modules.get(module_name) if isinstance(module_name, str) else None
    if module is None or not parts or "<locals>" in parts:
        return None
    found: object | None = module
    for part in parts:
        found = attr_of(found, part) if found is not None else None
        if found is None:
            return None
    return found if isinstance(found, type) else None


def enclosing_class(obj: object) -> type | None:
    """The class a test function belongs to.

    For a bound method this is the class of the instance. For a plain function
    it is resolved from ``__qualname__``, which works for classes at module
    level but not for classes defined inside functions.
    """
    if inspect.ismethod(obj):
        owner = obj.__self__
        return owner if isinstance(owner, type) else type(owner)
    for item in wrapped_chain(obj):
        qualname = attr_of(item, "__qualname__")
        if isinstance(qualname, str):
            return _class_at(attr_of(item, "__module__"), qualname.split(".")[:-1])
    return None


def parent_class(cls: type) -> type | None:
    """The class *cls* is nested in, resolved from ``__qualname__``."""
    return _class_at(cls.__module__, cls.__qualname__.split(".")[:-1])


def root_class(cls: type) -> type:
    """The outermost class *cls* is nested in (the contract), or *cls* itself."""
    current = cls
    while True:
        parent = parent_class(current)
        if parent is None:
            return current
        current = parent


def functions_in(obj: object) -> Iterator[object]:
    """The functions of a class (including static and class methods), or *obj* itself."""
    if isinstance(obj, type):
        for value in namespace_of(obj).values():
            unwrapped = attr_of(value, "__func__")  # staticmethod / classmethod
            function = value if unwrapped is None else unwrapped
            if inspect.isfunction(function):
                yield function
    elif inspect.isfunction(obj):
        yield obj


def iter_tests(within: Iterable[object]) -> Iterator[object]:
    """The test functions found in modules, classes or functions (each once)."""
    seen: set[int] = set()
    for item in within:
        candidates: Iterable[object] = (
            namespace_of(item).values() if isinstance(item, ModuleType) else (item,)
        )
        for candidate in candidates:
            for function in functions_in(candidate):
                if id(function) not in seen:
                    seen.add(id(function))
                    yield function
