"""Descriptors, relation words, annotation words and the ``binds`` decorator."""

from __future__ import annotations

import types
from collections.abc import Callable
from typing import Annotated, Generic, Self, TypeVar, cast, overload

from shikumi_contrace._model import (
    ANNOTATION,
    BINDING,
    RELATION,
    AnnotationValue,
    Binding,
    Form,
    Relation,
    Word,
    attach,
    attr_of,
    origin_of,
    record_use,
    type_args,
)
from shikumi_contrace._shikumi import ClassBinding, InformationType, class_binding

T = TypeVar("T")
# What a declaration can be attached to: a function, a method, or a class.
F = TypeVar("F", bound="Callable[..., object] | type")


def _is_text(value: object) -> bool:
    return isinstance(value, str)


def _is_class(value: object) -> bool:
    return isinstance(value, type)


def _is_target(value: object) -> bool:
    return callable(value) or isinstance(value, type)


# Special forms that are classes at run time but are not generic classes.
_SPECIAL_FORM_ORIGINS: tuple[object, ...] = (types.UnionType, Annotated)


def _subject_class(argument: object) -> type | None:
    """The class that a type argument of ``binds`` stands for (SYN_016, SYN_027).

    That is the class itself, or the class behind a generic class that was given
    type arguments (``Subject[Handle]`` stands for ``Subject``). Unions and the
    other special forms stand for no class.
    """
    if isinstance(argument, type):
        return argument
    origin = origin_of(argument)
    if isinstance(origin, type) and origin not in _SPECIAL_FORM_ORIGINS:
        return origin
    return None


def _class_body_binding(binding: ClassBinding[T]) -> object:
    """Hide the type of the temporary class-body binding (see ``__imatmul__``)."""
    return binding


class ClassBodyDescriptor(Generic[T]):
    """A descriptor written as ``name @= value`` in a class body (SYN_001).

    The value is checked when ``@=`` is evaluated. Nothing raises while the
    class is being created (SYN_021): Python 3.11 would wrap such an exception
    in ``RuntimeError``.
    """

    def __init__(
        self,
        information_type: InformationType[T],
        check: Callable[[T], str | None],
    ) -> None:
        self._information_type: InformationType[T] = information_type
        self._check: Callable[[T], str | None] = check

    def __imatmul__(self, value: T) -> Self:
        # Typed as `Self`: in a class body `name @= value` rebinds `name`, and
        # type checkers (mypy) require the result to have the type of `name`.
        # At run time the result is a temporary binding that Shikumi removes
        # again when the class is created (SYN_024).
        problem = self._check(value)
        if problem is not None:
            raise TypeError(problem)
        return cast("Self", _class_body_binding(class_binding(value, self._connect)))

    def _connect(self, owner: type[object], value: T) -> None:
        record_use(owner, self)
        attach(owner, self._information_type, value)


class AnnotationWord:
    """An annotation word. One word works in every form (SYN_006).

    ``rationale @= "text"`` in a class body, ``@rationale("text")`` and the bare
    ``@critical`` before a target all attach the same information.
    """

    def __init__(self, name: str) -> None:
        self.word: Word = Word(name, "annotation")

    def __imatmul__(self, text: str) -> Self:
        if not _is_text(text):
            raise TypeError(f"{self.word.name} @= needs a text, got {text!r}")
        return cast("Self", _class_body_binding(class_binding(text, self._connect)))

    def _connect(self, owner: type[object], text: str) -> None:
        _ = self._apply(owner, text, "body")

    @overload
    def __call__(self, target: F, /) -> F: ...

    @overload
    def __call__(self, text: str, /) -> Callable[[F], F]: ...

    def __call__(self, arg: str | F, /) -> Callable[[F], F] | F:
        if isinstance(arg, str):
            text = arg

            def decorate(target: F) -> F:
                return self._apply(target, text, "decorator")

            return decorate
        if not _is_target(arg):
            raise TypeError(
                f"@{self.word.name} takes a text or the target itself, got {arg!r}"
            )
        return self._apply(arg, None, "decorator")

    def _apply(self, target: F, text: str | None, form: Form) -> F:
        record_use(target, self)
        # `form` lets the reading API return annotations in the order they were written.
        attach(target, ANNOTATION, AnnotationValue(self.word, text, form))
        return target


class RelationWord:
    """A relation word: a decorator taking clause classes (SYN_008, SYN_009, SYN_010)."""

    def __init__(self, name: str) -> None:
        self.word: Word = Word(name, "relation")

    def __call__(self, *clauses: type[object]) -> Callable[[F], F]:
        if not clauses:
            raise TypeError(f"{self.word.name}() needs at least one clause")
        for clause in clauses:
            if not _is_class(clause):
                raise TypeError(
                    f"{self.word.name}() takes clause classes, not {clause!r}"
                )

        def decorate(target: F) -> F:
            if _is_class(target):
                raise TypeError(
                    f"{self.word.name}() applies to test functions and methods, not to a class"
                )
            record_use(target, self)
            # The reading API reverses what decorators attached (they apply bottom up).
            # Attaching the clauses of one call in reverse keeps their written order.
            for clause in reversed(clauses):
                attach(target, RELATION, Relation(self.word, clause))
            return target

        return decorate


class binds(Generic[T]):
    """Bind a subject type to implementations: ``@binds[Subject](Impl)``.

    The subject type is the type argument, so a type checker can verify that
    every implementation conforms to it (SYN_016, SYN_019). An implementation is
    something that produces the subject type (a class or a factory function) or
    the subject type itself (a function, a module, an object) (SYN_017).

    The subject type may be a generic class given type arguments
    (``@binds[Inventory[Reservation]](Impl)``). The type checker uses the type
    arguments; the binding records only the class (SYN_027).
    """

    def __init__(self, *implementations: T | Callable[..., T]) -> None:
        if not implementations:
            raise TypeError("binds needs at least one implementation")
        self._implementations: tuple[T | Callable[..., T], ...] = implementations

    def __call__(self, target: F) -> F:
        arguments = type_args(attr_of(self, "__orig_class__"))
        subject = _subject_class(arguments[0]) if arguments else None
        if subject is None:
            raise TypeError(
                "binds needs the subject type (a class) as a type argument: binds[Subject](Impl). "
                + "Without it a type checker cannot check that the implementation conforms."
            )
        record_use(target, self)
        # Reversed, for the same reason as in RelationWord: the reading API restores the written order.
        for implementation in reversed(self._implementations):
            attach(target, BINDING, Binding(subject, implementation))
        return target
