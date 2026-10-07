"""What a user's type checker must accept, and must reject.

Every ``# pyright: ignore`` below marks a line that must be an error. With
``reportUnnecessaryTypeIgnoreComment`` a missing error fails the check.
"""

from __future__ import annotations

import datetime
from typing import Protocol, TypeVar, overload

import slugs_bad
import slugs_ok

from shikumi_contrace import (
    OUT_OF_SCOPE,
    POST,
    PRE,
    REJECTED,
    binds,
    boundary,
    critical,
    define,
    depends_on,
    kind,
    member,
    note,
    on_violation,
    rationale,
    security,
    subject,
    upholds,
    violates,
)

T = TypeVar("T")


class User(Protocol):
    @property
    def username(self) -> str: ...


class UserService(Protocol):
    def register(self, username: str, *, at: datetime.date) -> User: ...


class Slugify(Protocol):
    def __call__(self, text: str, *, max_length: int = 80) -> str: ...


class BaseContract:
    subject @= UserService


class Contract:
    subject @= UserService
    depends_on @= BaseContract

    class register:
        member @= UserService.register
        note @= "text"
        rationale @= "reason"

        @critical
        @security
        class Clause:
            """A clause."""

            kind @= PRE
            on_violation @= REJECTED

        class After:
            """Another clause."""

            kind @= POST


class CallableContract:
    subject @= Slugify
    member @= Slugify.__call__

    class NonEmpty:
        kind @= PRE
        on_violation @= OUT_OF_SCOPE


# --- implementations ---------------------------------------------------------
class GoodUser:
    username: str = ""
    extra: int = 0  # more than the contract asks for is fine


class GoodImpl:
    def register(self, username: str, *, at: datetime.date) -> GoodUser:
        return GoodUser()


class WrongImpl:
    def register(self, username: str) -> None: ...  # no `at`, wrong return type


def good_slugify(text: str, *, max_length: int = 80) -> str:
    return text


def bad_slugify(text: str) -> str:
    return text


# --- accepted ----------------------------------------------------------------
@binds[UserService](GoodImpl)
class TestsGood:
    @upholds(Contract.register.Clause, Contract.register.After)
    @violates(Contract.register.Clause)
    @boundary
    @note("text")
    def test_x(self) -> None: ...


@binds[Slugify](good_slugify)
class TestsFunction: ...


flaky = define.annotation("flaky")
quarantines = define.relation("quarantines")


@flaky("custom")
@quarantines(Contract.register.Clause)
def test_custom() -> None: ...


# --- rejected ----------------------------------------------------------------
@binds[UserService](WrongImpl)  # pyright: ignore
class TestsWrong: ...


@binds[Slugify](bad_slugify)  # pyright: ignore
class TestsWrongFunction: ...


@upholds("Contract.register.Clause")  # pyright: ignore
def test_string_instead_of_clause() -> None: ...


class BadValues:
    kind @= "pre"  # pyright: ignore
    note @= 3  # pyright: ignore
    depends_on @= "Contract"  # pyright: ignore
    on_violation @= "rejected"  # pyright: ignore


# --- a module as the implementation (CTR_013) --------------------------------
class SlugTools(Protocol):
    def slugify(self, text: str) -> str: ...
    def unslugify(self, slug: str) -> str: ...


@binds[SlugTools](slugs_ok)
class TestsModule: ...


@binds[SlugTools](slugs_bad)  # pyright: ignore
class TestsBadModule: ...


# --- generic and overloaded functions (NOTICE_022) ---------------------------
class Identity(Protocol):
    def __call__(self, value: T) -> T: ...


class Parse(Protocol):
    @overload
    def __call__(self, text: str) -> int: ...
    @overload
    def __call__(self, text: bytes) -> int: ...


def identity(value: T) -> T:
    return value


def int_identity(value: int) -> int:
    return value


@overload
def parse(text: str) -> int: ...
@overload
def parse(text: bytes) -> int: ...
def parse(text: str | bytes) -> int:
    return 0


def parse_str_only(text: str) -> int:
    return 0


@binds[Identity](identity)
class TestsGeneric: ...


@binds[Identity](int_identity)  # pyright: ignore
class TestsNotGeneric: ...


@binds[Parse](parse)
class TestsOverloaded: ...


@binds[Parse](parse_str_only)  # pyright: ignore
class TestsNotOverloaded: ...


# --- a generic subject: an opaque handle (SYN_027) ---------------------------
class Handle(Protocol):
    @property
    def key(self) -> str: ...


H = TypeVar("H", bound=Handle)


class Store(Protocol[H]):
    def open(self) -> H: ...
    def close(self, handle: H) -> None: ...


class Door:
    key: str = ""


class DoorStore:
    def open(self) -> Door:
        return Door()

    def close(self, handle: Door) -> None: ...


class LeakyStore:
    def open(self) -> Door:
        return Door()

    def close(self, handle: str) -> None: ...  # does not take back what it hands out


class OtherDoor:
    key: str = ""


class OtherStore:
    def open(self) -> OtherDoor:
        return OtherDoor()

    def close(self, handle: OtherDoor) -> None: ...


@binds[Store[Door]](DoorStore)
class TestsGenericSubject: ...


@binds[Store[Door]](LeakyStore)  # pyright: ignore
class TestsLeakyStore: ...


@binds[Store[Door]](OtherStore)  # pyright: ignore
class TestsOtherHandle: ...
