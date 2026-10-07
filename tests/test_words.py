"""Relation words, annotation words and custom words (SYN_005-009, SYN_012, STD_*)."""

from __future__ import annotations

import pytest

from shikumi_contrace import (
    OUT_OF_SCOPE,
    boundary,
    critical,
    define,
    note,
    rationale,
    security,
    upholds,
    violates,
)
from shikumi_contrace.reading import annotations_of, relations_of


class Clause:
    """A clause."""


class Other:
    """Another clause."""


def test_a_relation_word_attaches_one_relation_per_clause():
    @upholds(Clause, Other)
    def test_x(): ...

    assert [r.clause for r in relations_of(test_x)] == [Clause, Other]
    assert {r.word.name for r in relations_of(test_x)} == {"upholds"}


def test_relation_words_stack():
    @violates(Clause)
    @upholds(Other)
    def test_x(): ...

    assert {r.word.name for r in relations_of(test_x)} == {"upholds", "violates"}


def test_a_relation_word_takes_classes_not_strings():  # SYN_009
    with pytest.raises(TypeError):
        upholds("Contract.Clause")  # type: ignore[arg-type]


def test_a_relation_word_needs_a_clause():
    with pytest.raises(TypeError):
        upholds()


def test_annotation_words_work_as_decorators_with_and_without_text():  # SYN_006, SYN_007
    @security
    @rationale("because")
    @boundary
    def test_x(): ...

    found = {(a.word.name, a.text) for a in annotations_of(test_x)}
    assert found == {("security", None), ("rationale", "because"), ("boundary", None)}


def test_the_decorator_form_works_on_classes_too():
    @critical
    @note("text")
    class Target: ...

    assert {a.word.name for a in annotations_of(Target)} == {"critical", "note"}


def test_all_forms_attach_the_same_information():
    class A:
        note @= "same"

    @note("same")
    class B: ...

    assert annotations_of(A) == annotations_of(B)


def test_an_annotation_decorator_rejects_other_arguments():
    with pytest.raises(TypeError):
        note(3)  # type: ignore[call-overload]


def test_custom_words_are_made_by_the_same_generators():  # SYN_012, VOC_003
    flaky = define.annotation("flaky")
    quarantines = define.relation("quarantines")
    coerced = define.violation("coerced")

    @flaky("clock dependent")
    @quarantines(Clause)
    def test_x(): ...

    assert [a.word.name for a in annotations_of(test_x)] == ["flaky"]
    assert [r.word.name for r in relations_of(test_x)] == ["quarantines"]
    assert coerced.category == "violation"
    assert coerced != OUT_OF_SCOPE


def test_custom_words_are_equal_when_name_and_category_are_equal():
    assert define.kind("x") == define.kind("x")
    assert define.kind("x") != define.annotation("x").word
    assert define.violation("x") == define.violation("x")
    assert define.violation("x") != define.kind("x")


@pytest.mark.parametrize(
    "make", [define.relation, define.annotation, define.kind, define.violation]
)
@pytest.mark.parametrize("bad", ["", "  ", None, 3])
def test_a_word_needs_a_name(make, bad):
    with pytest.raises(TypeError):
        make(bad)


def test_a_relation_word_cannot_decorate_a_class():  # SYN_010
    with pytest.raises(TypeError, match="functions and methods"):

        @upholds(Clause)  # type: ignore[type-var]
        class TestIt: ...
