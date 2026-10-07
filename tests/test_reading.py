"""The reading API (RDG_001-RDG_010, API_004, API_005)."""

from __future__ import annotations

import functools
from typing import Protocol
from unittest import mock

import pytest

from shikumi_contrace import (
    INV,
    OUT_OF_SCOPE,
    POST,
    PRE,
    REJECTED,
    binds,
    critical,
    define,
    depends_on,
    kind,
    member,
    note,
    on_violation,
    rationale,
    reading,
    subject,
    upholds,
    violates,
)
from shikumi_contrace.reading import (
    Annotation,
    Binding,
    Clause,
    Relation,
    annotations_of,
    bindings_of,
    clauses_of,
    dependencies_of,
    dependents_of,
    relations_of,
    untested_clauses,
)


class Service(Protocol):
    def run(self) -> int: ...


class Impl:
    def run(self) -> int:
        return 1


class Contract:
    subject @= Service

    class Stable:
        """The state is stable."""

        kind @= INV

    class run:
        member @= Service.run
        note @= "about run"

        @critical
        class Positive:
            """The result is positive."""

            kind @= POST
            rationale @= "reason"

        class Needs:
            """Needs something."""

            kind @= PRE
            on_violation @= REJECTED


CLAMPED = define.violation("clamped")


class ScopedContract:
    subject @= Service

    class run:
        member @= Service.run

        class Authenticated:
            """The caller is authenticated."""

            kind @= PRE
            on_violation @= OUT_OF_SCOPE

        class Positive:
            """The input is positive."""

            kind @= PRE
            on_violation @= REJECTED

        class Limited:
            """The input is below the limit."""

            kind @= PRE

        class Clamped:
            """The input is in range."""

            kind @= PRE
            on_violation @= CLAMPED

        class Calm:
            """The caller is not in a hurry."""

            kind @= PRE
            on_violation @= OUT_OF_SCOPE


class OtherContract:
    subject @= Service


class DependentContract:
    subject @= Service
    depends_on @= Contract
    depends_on @= OtherContract


def test_contract_dependencies_are_read_in_written_order():  # RDG_010
    assert dependencies_of(DependentContract) == (Contract, OtherContract)


def test_contract_dependents_are_reverse_looked_up_within_a_scope():  # RDG_010
    import sys

    assert dependents_of(Contract, within=[sys.modules[__name__]]) == (
        DependentContract,
    )


def test_clauses_are_listed_in_definition_order_with_kind_statement_and_notes():  # RDG_003
    clauses = clauses_of(Contract)
    assert [c.path for c in clauses] == ["Stable", "run.Positive", "run.Needs"]
    assert [c.kind for c in clauses] == [INV, POST, PRE]
    assert [c.on_violation for c in clauses] == [None, None, REJECTED]
    assert clauses[1].statement == "The result is positive."
    assert {a.word.name for a in clauses[1].annotations} == {"critical", "rationale"}
    assert all(isinstance(c, Clause) for c in clauses)


def test_the_member_class_is_not_a_clause():
    assert Contract.run not in [c.cls for c in clauses_of(Contract)]
    assert [a.text for a in annotations_of(Contract.run)] == ["about run"]


def test_a_test_declares_relations_notes_and_bindings():  # RDG_002
    @binds[Service](Impl)
    @note("boundary case")
    @violates(Contract.run.Needs)
    @upholds(Contract.Stable)
    def test_x(): ...

    relations = relations_of(test_x)
    assert {(r.word.name, r.clause) for r in relations} == {
        ("violates", Contract.run.Needs),
        ("upholds", Contract.Stable),
    }
    assert all(isinstance(r, Relation) for r in relations)
    assert annotations_of(test_x) == (Annotation(note.word, "boundary case"),)
    assert bindings_of(test_x) == (Binding(Service, Impl),)


@binds[Service](Impl)
class BoundSuite:
    def test_a(self): ...


class OtherImpl(Impl): ...


@binds[Service](Impl)
class MixedSuite:
    @binds[Service](OtherImpl)
    def test_a(self): ...


def test_a_binding_on_the_class_is_a_binding_of_its_tests():  # SYN_018, RDG_002
    assert bindings_of(BoundSuite) == (Binding(Service, Impl),)
    assert bindings_of(BoundSuite.test_a) == (Binding(Service, Impl),)


def test_bindings_on_both_the_class_and_the_method_apply_together():  # SYN_018
    found = {b.implementation for b in bindings_of(MixedSuite.test_a)}
    assert found == {Impl, OtherImpl}


def test_tests_are_looked_up_from_a_clause(project):  # RDG_004
    project.write(
        {
            "tm.py": """
            from shikumi_contrace import upholds
            from tests_support import Contract

            class TestA:
                @upholds(Contract.run.Positive)
                def test_one(self): ...
                def test_unrelated(self): ...

            @upholds(Contract.run.Positive, Contract.Stable)
            def test_two(): ...
            """,
        }
    )
    import sys

    sys.modules["tests_support"] = sys.modules[__name__]
    try:
        module = project.load("tm")
        found = reading.tests_of(Contract.run.Positive, within=[module])
        assert {t.__name__ for t in found} == {"test_one", "test_two"}  # type: ignore[attr-defined]
        # a Clause object works as well as the class
        clause = next(c for c in clauses_of(Contract) if c.cls is Contract.run.Positive)
        assert reading.tests_of(clause, within=[module]) == found
    finally:
        del sys.modules["tests_support"]


def test_clauses_without_a_test_are_listed(project):  # RDG_005
    project.write(
        {
            "tm2.py": """
            from shikumi_contrace import upholds
            from tests_support import Contract

            @upholds(Contract.Stable)
            def test_stable(): ...
            """,
        }
    )
    import sys

    sys.modules["tests_support"] = sys.modules[__name__]
    try:
        module = project.load("tm2")
        missing = untested_clauses(Contract, within=[module])
        assert [c.path for c in missing] == ["run.Positive", "run.Needs"]
    finally:
        del sys.modules["tests_support"]


def _paths(clauses):
    return [c.path for c in clauses]


def test_violation_behavior_does_not_change_untested_listing():  # RDG_005
    assert _paths(untested_clauses(ScopedContract)) == [
        "run.Authenticated",
        "run.Positive",
        "run.Limited",
        "run.Clamped",
        "run.Calm",
    ]


def test_tested_clauses_are_not_listed_regardless_of_violation_behavior():  # RDG_005
    @violates(ScopedContract.run.Positive)
    @violates(ScopedContract.run.Calm)
    def test_it(): ...

    listed = untested_clauses(ScopedContract, within=[test_it])
    assert "run.Positive" not in _paths(listed)
    assert "run.Calm" not in _paths(listed)


def test_nothing_is_modified_by_reading():  # RDG_006
    before = relations_of(Contract), annotations_of(Contract.run), clauses_of(Contract)
    relations_of(Contract), annotations_of(Contract.run), clauses_of(Contract)
    assert before == (
        relations_of(Contract),
        annotations_of(Contract.run),
        clauses_of(Contract),
    )


def _passthrough(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)

    return wrapper


@pytest.mark.parametrize(
    "order",
    ["declaration-outside", "declaration-inside"],
)
def test_declarations_survive_other_decorators(order):  # RDG_007
    if order == "declaration-outside":

        @upholds(Contract.Stable)
        @_passthrough
        def test_x(): ...

    else:

        @_passthrough
        @upholds(Contract.Stable)
        def test_x(): ...

    assert [r.clause for r in relations_of(test_x)] == [Contract.Stable]


def test_declarations_below_mock_patch_are_found():  # RDG_007
    @mock.patch("os.getcwd")
    @upholds(Contract.Stable)
    def test_x(patched): ...

    assert [r.clause for r in relations_of(test_x)] == [Contract.Stable]


def test_declarations_on_both_wrapper_and_inner_function_are_both_returned():  # RDG_007
    @upholds(Contract.Stable)
    @_passthrough
    @violates(Contract.run.Needs)
    def test_x(): ...

    assert {r.clause for r in relations_of(test_x)} == {
        Contract.Stable,
        Contract.run.Needs,
    }


def test_bound_methods_are_read_through_their_function():
    class TestIt:
        @upholds(Contract.Stable)
        def test_a(self): ...

    assert [r.clause for r in relations_of(TestIt().test_a)] == [Contract.Stable]


def test_tests_of_is_not_collected_as_a_test_when_imported(pytester):
    # `tests_of` starts with "test"; importing it must not create a test.
    pytester.makepyfile(
        """
        from shikumi_contrace.reading import tests_of

        def test_real():
            assert callable(tests_of)
        """
    )
    result = pytester.runpytest_subprocess()
    result.assert_outcomes(passed=1)


def test_relations_are_returned_in_the_order_they_are_written():  # RDG_009
    @upholds(Contract.Stable)  # written first (top)
    @violates(Contract.run.Needs)
    @upholds(Contract.run.Positive)  # written last (bottom)
    def test_x(): ...

    assert [r.clause for r in relations_of(test_x)] == [
        Contract.Stable,
        Contract.run.Needs,
        Contract.run.Positive,
    ]


def test_annotations_are_returned_decorators_first_then_the_body_of_a_class():  # RDG_009
    @critical
    @note("second decorator")
    class Clause:
        note @= "body one"
        rationale @= "body two"

    assert [(a.word.name, a.text) for a in annotations_of(Clause)] == [
        ("critical", None),
        ("note", "second decorator"),
        ("note", "body one"),
        ("rationale", "body two"),
    ]


def test_information_of_an_outer_wrapper_comes_before_the_inner_function():  # RDG_007, RDG_009
    @upholds(Contract.Stable)
    @_passthrough
    @violates(Contract.run.Needs)
    def test_x(): ...

    assert [r.clause for r in relations_of(test_x)] == [
        Contract.Stable,
        Contract.run.Needs,
    ]


def test_the_class_of_a_bound_method_is_found_even_for_local_classes():  # RDG_002
    @binds[Service](Impl)
    class LocalSuite:
        def test_a(self): ...

    assert bindings_of(LocalSuite().test_a) == (Binding(Service, Impl),)
    # From the plain function the class cannot be resolved (it is defined in a function).
    assert bindings_of(LocalSuite.test_a) == ()


def test_clauses_given_to_one_relation_word_keep_their_written_order():  # RDG_009
    @upholds(Contract.Stable, Contract.run.Needs)  # written first (top), left to right
    @violates(Contract.run.Positive)
    def test_x(): ...

    assert [r.clause for r in relations_of(test_x)] == [
        Contract.Stable,
        Contract.run.Needs,
        Contract.run.Positive,
    ]


def test_implementations_given_to_binds_keep_their_written_order():  # RDG_009
    class FirstImpl(Impl): ...

    class SecondImpl(Impl): ...

    @binds[Service](FirstImpl, SecondImpl)  # written first (top), left to right
    @binds[Service](Impl)
    class Suite: ...

    assert [b.implementation for b in bindings_of(Suite)] == [
        FirstImpl,
        SecondImpl,
        Impl,
    ]
