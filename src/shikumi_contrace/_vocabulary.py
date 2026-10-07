"""The standard vocabulary and the generators for custom words (SYN_012)."""

from __future__ import annotations

from shikumi_contrace._descriptors import (
    AnnotationWord,
    ClassBodyDescriptor,
    RelationWord,
)
from shikumi_contrace._model import (
    DEPENDENCY,
    KIND,
    MEMBER,
    ON_VIOLATION,
    SUBJECT,
    Word,
)


def _check_subject(value: object) -> str | None:
    if not isinstance(value, type):
        return f"subject @= needs a type (a class), got {value!r}"
    return None


def _check_member(value: object) -> str | None:
    if not callable(value):
        return f"member @= needs a reference to a member of the subject type, got {value!r}"
    return None


def _check_kind(value: object) -> str | None:
    if not isinstance(value, Word) or value.category != "kind":
        return f"kind @= needs a clause kind such as PRE, POST or INV, got {value!r}"
    return None


def _check_dependency(value: object) -> str | None:
    if not isinstance(value, type):
        return f"depends_on @= needs a contract class, got {value!r}"
    return None


def _check_violation_behavior(value: object) -> str | None:
    if not isinstance(value, Word) or value.category != "violation":
        return (
            "on_violation @= needs a violation behavior such as "
            f"OUT_OF_SCOPE or REJECTED, got {value!r}"
        )
    return None


def _check_name(name: object) -> str:
    if not isinstance(name, str) or not name.strip():
        raise TypeError(f"a word needs a non-empty name, got {name!r}")
    return name


class _Define:
    """Generators for custom words. Standard words are made the same way."""

    @staticmethod
    def relation(name: str) -> RelationWord:
        return RelationWord(_check_name(name))

    @staticmethod
    def annotation(name: str) -> AnnotationWord:
        return AnnotationWord(_check_name(name))

    @staticmethod
    def kind(name: str) -> Word:
        return Word(_check_name(name), "kind")

    @staticmethod
    def violation(name: str) -> Word:
        return Word(_check_name(name), "violation")


define = _Define()

# Descriptors written as `name @= value` in a class body.
subject = ClassBodyDescriptor[type](SUBJECT, _check_subject)
member = ClassBodyDescriptor[object](MEMBER, _check_member)
kind = ClassBodyDescriptor[Word](KIND, _check_kind)
depends_on = ClassBodyDescriptor[type](DEPENDENCY, _check_dependency)
on_violation = ClassBodyDescriptor[Word](ON_VIOLATION, _check_violation_behavior)

# Clause kinds.
PRE = define.kind("pre")
POST = define.kind("post")
INV = define.kind("inv")

# What a PRE clause promises about a violating call. These values deliberately
# say nothing about the implementation mechanism (exception, result value,
# protocol response, ...).
OUT_OF_SCOPE = define.violation("out_of_scope")
REJECTED = define.violation("rejected")

# Relation words.
upholds = define.relation("upholds")
violates = define.relation("violates")

# Annotation words.
note = define.annotation("note")
rationale = define.annotation("rationale")
caution = define.annotation("caution")
example = define.annotation("example")
source = define.annotation("source")
assumption = define.annotation("assumption")
security = define.annotation("security")
performance = define.annotation("performance")
concurrency = define.annotation("concurrency")
critical = define.annotation("critical")
todo = define.annotation("todo")
provisional = define.annotation("provisional")
legacy = define.annotation("legacy")
deprecated = define.annotation("deprecated")
manual = define.annotation("manual")
boundary = define.annotation("boundary")
regression = define.annotation("regression")
