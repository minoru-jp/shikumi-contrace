"""The binding decorator binds[Subject](implementation) (SYN_015-018, SYN_020)."""

from __future__ import annotations

import types
from typing import Annotated, Literal, Protocol, TypeVar

import pytest

from shikumi_contrace import binds
from shikumi_contrace._model import BINDING, infos_on
from shikumi_contrace.reading import Binding, bindings_of


class Spec(Protocol):
    def run(self) -> int: ...


class Impl:
    def run(self) -> int:
        return 1


def make_impl() -> Impl:
    return Impl()


def function_impl() -> int:  # a function as the implementation of a callable subject
    return 1


module_impl = types.ModuleType("module_impl")


def test_binds_records_the_subject_type_and_the_implementations():
    @binds[Spec](Impl, make_impl)
    class TestIt: ...

    assert bindings_of(TestIt) == (Binding(Spec, Impl), Binding(Spec, make_impl))


def test_binds_works_on_functions_and_methods():
    @binds[Spec](Impl)
    def test_x(): ...

    assert infos_on(test_x, BINDING) == (Binding(Spec, Impl),)


def test_an_implementation_can_be_a_function_or_a_module():  # SYN_017
    @binds[Spec](function_impl, module_impl)  # type: ignore[arg-type]
    class TestIt: ...

    assert [b.implementation for b in bindings_of(TestIt)] == [
        function_impl,
        module_impl,
    ]


def test_the_subject_type_argument_is_required():  # SYN_016
    with pytest.raises(TypeError, match="type argument"):

        @binds(Impl)  # type: ignore[arg-type]
        class TestIt: ...


def test_at_least_one_implementation_is_required():
    with pytest.raises(TypeError):
        binds[Spec]()


def test_binds_returns_the_decorated_target_unchanged():  # PYT-level: tests are not rewritten
    class TestIt:
        def test_x(self): ...

    assert binds[Spec](Impl)(TestIt) is TestIt


@pytest.mark.parametrize(
    "not_a_class",
    [int | str, Spec | None, Annotated[Spec, "x"], Literal[1], "Spec", 3],
)
def test_the_type_argument_must_be_a_class(not_a_class):  # SYN_016
    with pytest.raises(TypeError, match="type argument"):

        @binds[not_a_class](Impl)  # type: ignore[valid-type]
        class TestIt: ...


# --- a generic subject (SYN_027) ----------------------------------------------
Handle = TypeVar("Handle")


class Store(Protocol[Handle]):
    def open(self) -> Handle: ...

    def close(self, handle: Handle) -> None: ...


class Door:
    pass


class DoorStore:
    def open(self) -> Door:
        return Door()

    def close(self, handle: Door) -> None: ...


def test_a_generic_subject_is_recorded_as_its_class():  # SYN_027
    @binds[Store[Door]](DoorStore)
    class TestIt: ...

    assert bindings_of(TestIt) == (Binding(Store, DoorStore),)


def test_the_unparametrized_generic_class_is_accepted_too():  # SYN_027
    @binds[Store](DoorStore)  # type: ignore[type-arg]
    class TestIt: ...

    assert bindings_of(TestIt) == (Binding(Store, DoorStore),)


def test_a_parametrized_ordinary_class_stands_for_its_class():  # SYN_027
    @binds[list[int]](list)
    class TestIt: ...

    assert bindings_of(TestIt) == (Binding(list, list),)


def test_bindings_with_different_type_arguments_share_the_subject():  # SYN_027
    @binds[Store[Door]](DoorStore)
    class TestDoors: ...

    @binds[Store[int]](DoorStore)  # type: ignore[type-var]
    class TestInts: ...

    assert bindings_of(TestDoors)[0].subject is bindings_of(TestInts)[0].subject
