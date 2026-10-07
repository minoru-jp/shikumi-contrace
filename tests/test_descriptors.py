"""The class-body descriptors subject, member and kind (SYN_002-004, SYN_021)."""

from __future__ import annotations

from typing import Protocol

import pytest

from shikumi_contrace import (
    INV,
    OUT_OF_SCOPE,
    POST,
    PRE,
    REJECTED,
    define,
    depends_on,
    kind,
    member,
    note,
    on_violation,
    subject,
)
from shikumi_contrace._model import (
    DEPENDENCY,
    KIND,
    MEMBER,
    ON_VIOLATION,
    SUBJECT,
    infos_on,
)
from shikumi_contrace.reading import annotations_of


class Service(Protocol):
    def run(self, x: int) -> int: ...


def test_subject_member_and_kind_attach_information():
    class Contract:
        subject @= Service

        class run:
            member @= Service.run

            class Positive:
                """x is positive."""

                kind @= PRE

    assert infos_on(Contract, SUBJECT) == (Service,)
    assert infos_on(Contract.run, MEMBER) == (Service.run,)
    assert infos_on(Contract.run.Positive, KIND) == (PRE,)


def test_descriptors_leave_no_attribute_in_the_class():
    class Contract:
        subject @= Service
        note @= "n"

    assert not hasattr(Contract, "subject")
    assert not hasattr(Contract, "note")


def test_the_same_word_can_be_written_repeatedly():
    class Clause:
        kind @= POST
        note @= "first"
        note @= "second"

    assert [a.text for a in annotations_of(Clause)] == ["first", "second"]


def test_contract_dependencies_can_be_written_repeatedly_in_order():  # SYN_025
    class BaseA:
        subject @= Service

    class BaseB:
        subject @= Service

    class Contract:
        subject @= Service
        depends_on @= BaseA
        depends_on @= BaseB

    assert infos_on(Contract, DEPENDENCY) == (BaseA, BaseB)
    assert not hasattr(Contract, "depends_on")


@pytest.mark.parametrize("behavior", [OUT_OF_SCOPE, REJECTED])
def test_precondition_violation_behavior_attaches_information(behavior):  # SYN_026
    class Clause:
        kind @= PRE
        on_violation @= behavior

    assert infos_on(Clause, ON_VIOLATION) == (behavior,)
    assert not hasattr(Clause, "on_violation")


def test_standard_and_custom_kinds_are_accepted():
    perf = define.kind("performance")

    class Clause:
        kind @= perf

    assert infos_on(Clause, KIND) == (perf,)
    assert perf != INV


@pytest.mark.parametrize(
    "define_class",
    [
        pytest.param(lambda: _make("subject", "123"), id="subject-needs-a-type"),
        pytest.param(lambda: _make("member", "42"), id="member-needs-a-reference"),
        pytest.param(lambda: _make("kind", "'pre'"), id="kind-needs-a-clause-kind"),
        pytest.param(lambda: _make("note", "3"), id="note-needs-a-text"),
        pytest.param(
            lambda: _make("depends_on", "'Contract'"),
            id="depends-on-needs-a-class",
        ),
        pytest.param(
            lambda: _make("on_violation", "'rejected'"),
            id="on-violation-needs-a-behavior",
        ),
    ],
)
def test_values_are_checked_when_at_equals_is_evaluated(define_class):
    # SYN_021: the error is a plain TypeError raised by the statement itself,
    # not an error raised while the class is being created.
    with pytest.raises(TypeError):
        define_class()


def _make(name: str, value: str) -> type:
    namespace: dict[str, object] = {
        "subject": subject,
        "member": member,
        "kind": kind,
        "note": note,
        "depends_on": depends_on,
        "on_violation": on_violation,
    }
    source = f"class Declared:\n    {name} @= {value}\n"
    exec(compile(source, "<test>", "exec"), namespace)  # noqa: S102
    return namespace["Declared"]  # type: ignore[return-value]
