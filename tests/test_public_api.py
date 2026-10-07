"""The public API: names, places and the independence of the core (API_001-003, PYT_006)."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import metamk
import pytest

import shikumi_contrace
import shikumi_contrace.checking
import shikumi_contrace.reading

ROOT = Path(__file__).resolve().parents[1]
STANDARD_VOCABULARY = (
    ROOT
    / "devdocs"
    / "canonical_documents"
    / "specification"
    / "standard_vocabulary.md"
)


def _standard_words(prefix: str) -> list[str]:
    text = STANDARD_VOCABULARY.read_text(encoding="utf-8")
    return re.findall(rf"^title: {prefix}: (\w+)$", text, re.MULTILINE)


def test_every_name_in_all_is_importable():
    for name in shikumi_contrace.__all__:
        assert hasattr(shikumi_contrace, name), name


def test_the_top_level_has_the_names_for_writing_only():
    # API_002 / API_003: reading and checking names are not at the top level.
    for name in (
        "relations_of",
        "clauses_of",
        "dependencies_of",
        "dependents_of",
        "tests_of",
        "check",
        "Diagnostic",
    ):
        assert not hasattr(shikumi_contrace, name), name
    for name in shikumi_contrace.reading.__all__ + shikumi_contrace.checking.__all__:
        assert name not in shikumi_contrace.__all__


def test_depends_on_is_a_top_level_writing_name():  # API_002
    assert "depends_on" in shikumi_contrace.__all__
    assert hasattr(shikumi_contrace, "depends_on")


def test_precondition_violation_names_are_top_level_writing_names():  # API_002
    assert "on_violation" in shikumi_contrace.__all__
    assert "OUT_OF_SCOPE" in shikumi_contrace.__all__
    assert "REJECTED" in shikumi_contrace.__all__


@pytest.mark.parametrize("word", _standard_words("Annotation word"))
def test_every_standard_annotation_word_of_the_specification_exists(word):
    assert word in shikumi_contrace.__all__
    assert getattr(shikumi_contrace, word).word.category == "annotation"


@pytest.mark.parametrize("word", _standard_words("Relation word"))
def test_every_standard_relation_word_of_the_specification_exists(word):
    assert getattr(shikumi_contrace, word).word.category == "relation"


@pytest.mark.parametrize("kind", _standard_words("Clause kind"))
def test_every_standard_clause_kind_of_the_specification_exists(kind):
    assert getattr(shikumi_contrace, kind).category == "kind"
    assert kind in shikumi_contrace.__all__


@pytest.mark.parametrize("behavior", _standard_words("Violation behavior"))
def test_every_standard_violation_behavior_of_the_specification_exists(behavior):
    assert getattr(shikumi_contrace, behavior).category == "violation"
    assert behavior in shikumi_contrace.__all__


def test_the_specification_lists_the_expected_number_of_standard_words():
    assert len(_standard_words("Annotation word")) == 17
    assert len(_standard_words("Relation word")) == 2
    assert len(_standard_words("Clause kind")) == 3
    assert len(_standard_words("Violation behavior")) == 2


def test_metamk_names_are_reexported_with_the_contrace_names(  # AIM_014, SYN_022
):
    assert shikumi_contrace.Phase is metamk.Mk
    assert shikumi_contrace.phase_of is metamk.phase_of
    assert "Phase" in shikumi_contrace.__all__
    assert "Mk" not in shikumi_contrace.__all__
    assert not hasattr(shikumi_contrace, "Mk")


def test_the_core_does_not_import_pytest():  # PYT_006
    code = (
        "import sys, shikumi_contrace, shikumi_contrace.reading, shikumi_contrace.checking;"
        "assert 'pytest' not in sys.modules, 'pytest was imported'"
    )
    completed = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=False
    )
    assert completed.returncode == 0, completed.stderr


def test_dependence_on_shikumi_is_in_one_module():  # REG_018
    offenders = [
        path.name
        for path in (ROOT / "src" / "shikumi_contrace").glob("*.py")
        if path.name != "_shikumi.py"
        and re.search(
            r"^\s*(from|import) shikumi\b",
            path.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
    ]
    assert offenders == []
