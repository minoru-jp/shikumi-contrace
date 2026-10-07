"""The checking API: ranges, independence and structure rules (REG_003-REG_020, API_006-007)."""

from __future__ import annotations

import pytest

from shikumi_contrace.checking import ContraceWarning, Diagnostic, check

IMPL = """
class UserService:
    def register(self, username: str, email: str) -> object: ...
"""

# A contract asset that lives inside the same top-level package as the implementation.
GOOD_CONTRACT = '''
from typing import Protocol
from shikumi_contrace import POST, PRE, kind, member, subject

class Spec(Protocol):
    def register(self, username: str, email: str) -> object: ...

class UserContract:
    subject @= Spec

    class register:
        member @= Spec.register

        class NeedsAt:
            """email contains an at sign."""
            kind @= PRE

        class Retrievable:
            """a registered user can be fetched."""
            kind @= POST
'''

LEAKY_CONTRACT = (
    GOOD_CONTRACT
    + """
from myproj.service import UserService as _Impl
"""
)

TESTS = """
from shikumi_contrace import binds, upholds, violates
from myproj.contracts.user import Spec, UserContract as C
from myproj.service import UserService

@binds[Spec](UserService)
class UserTests:
    @violates(C.register.NeedsAt)
    def test_a(self): ...
    @upholds(C.register.Retrievable)
    def test_b(self): ...
"""


@pytest.fixture
def tree(project):
    project.write(
        {
            "myproj/service.py": IMPL,
            "myproj/contracts/user.py": GOOD_CONTRACT,
            "tests_pkg/test_user.py": TESTS,
        }
    )
    return project


def codes(findings: list[Diagnostic]) -> list[str]:
    return sorted(f.code for f in findings)


def test_a_clean_project_has_no_findings_when_derived(tree):
    module = tree.load("tests_pkg.test_user")
    assert check(test_modules=[module]) == []


def test_a_contract_that_refers_to_an_implementation_is_reported(
    tree,
):  # IND_003, REG_003
    (tree.root / "myproj/contracts/user.py").write_text(
        LEAKY_CONTRACT, encoding="utf-8"
    )
    module = tree.load("tests_pkg.test_user")
    findings = check(test_modules=[module])
    assert codes(findings) == ["independence"]
    assert "implementations" in findings[0].message
    assert findings[0].subject.endswith("_Impl")


def test_a_contract_that_refers_to_a_test_is_reported(tree):  # IND_002
    source = GOOD_CONTRACT + "\nfrom tests_pkg import test_user as _tests\n"
    (tree.root / "myproj/contracts/user.py").write_text(source, encoding="utf-8")
    # The test module imports the contract, so import order matters: load tests first.
    findings = check(
        contract_assets=["myproj.contracts"],
        tests=["tests_pkg"],
        implementations=["myproj"],
    )
    assert "independence" in codes(findings)
    assert any("tests" in f.message for f in findings if f.code == "independence")


def test_derivation_leaves_out_standard_library_implementations(project):  # REG_012
    project.write(
        {
            "c.py": '''
            from typing import Protocol
            from shikumi_contrace import PRE, kind, member, subject

            class MapLike(Protocol):
                def get(self, key: str) -> object: ...

            class MapContract:
                subject @= MapLike

                class get:
                    member @= MapLike.get

                    class OnlyStr:
                        """keys are strings."""
                        kind @= PRE
                        text = str            # a reference to builtins
            ''',
            "t.py": """
            from shikumi_contrace import binds, upholds
            from c import MapLike, MapContract as C

            @binds[MapLike](dict)
            class MapTests:
                @upholds(C.get.OnlyStr)
                def test_a(self): ...
            """,
        }
    )
    assert check(test_modules=[project.load("t")]) == []


def test_the_longest_matching_range_wins(tree):  # REG_015
    # The contract asset is inside `myproj`, which is declared as the implementation.
    findings = check(
        contract_assets=["myproj.contracts"],
        tests=["tests_pkg"],
        implementations=["myproj"],
    )
    assert findings == []


def test_declared_ranges_cover_contracts_no_test_cites(tree):  # REG_014
    tree.write(
        {"myproj/contracts/orphan.py": "from myproj.service import UserService\n"}
    )
    findings = check(
        contract_assets=["myproj.contracts"],
        tests=["tests_pkg"],
        implementations=["myproj"],
    )
    assert codes(findings) == ["independence"]
    assert "orphan" in findings[0].subject


def test_declared_ranges_replace_derived_ones(tree):  # REG_011, API_007
    (tree.root / "myproj/contracts/user.py").write_text(
        LEAKY_CONTRACT, encoding="utf-8"
    )
    module = tree.load("tests_pkg.test_user")
    # Derived: the leak is found. Declared with only `tests`: the other roles are
    # empty, nothing is derived, and nothing is found.
    assert codes(check(test_modules=[module])) == ["independence"]
    assert "independence" not in codes(
        check(tests=["tests_pkg"], test_modules=[module])
    )


def test_a_clause_kind_in_the_wrong_place_is_reported(project):  # CTR_009, REG_004
    project.write(
        {
            "c.py": '''
            from typing import Protocol
            from shikumi_contrace import INV, POST, PRE, kind, member, subject

            class S(Protocol):
                def f(self) -> int: ...

            class Contract:
                subject @= S

                class MisplacedPre:
                    """pre directly under the contract."""
                    kind @= PRE

                class f:
                    member @= S.f

                    class MisplacedInv:
                        """inv under a member."""
                        kind @= INV
            ''',
            "t.py": """
            from shikumi_contrace import upholds
            from c import Contract as C

            @upholds(C.MisplacedPre, C.f.MisplacedInv)
            def test_x(): ...
            """,
        }
    )
    findings = [
        f for f in check(test_modules=[project.load("t")]) if f.code == "position"
    ]
    assert len(findings) == 2


def test_a_contract_that_stands_for_a_callable_member_may_hold_pre_and_post(
    project,
):  # CTR_012
    project.write(
        {
            "c.py": '''
            from typing import Protocol
            from shikumi_contrace import INV, POST, PRE, kind, member, subject

            class Slugify(Protocol):
                def __call__(self, text: str) -> str: ...

            class SlugContract:
                subject @= Slugify
                member @= Slugify.__call__

                class Ascii:
                    """output is ascii."""
                    kind @= POST

                class NotEmpty:
                    """text is not empty."""
                    kind @= PRE

                class Idempotent:
                    """slugifying twice changes nothing."""
                    kind @= INV
            ''',
            "t.py": """
            from shikumi_contrace import binds, upholds
            from c import Slugify, SlugContract as C

            def slugify(text: str) -> str:
                return text

            @binds[Slugify](slugify)
            class SlugTests:
                @upholds(C.Ascii, C.NotEmpty, C.Idempotent)
                def test_x(self): ...
            """,
        }
    )
    assert check(test_modules=[project.load("t")]) == []


def test_a_member_class_name_that_differs_from_its_member_is_reported(
    project,
):  # CTR_008, REG_005
    project.write(
        {
            "c.py": '''
            from typing import Protocol
            from shikumi_contrace import PRE, kind, member, subject

            class S(Protocol):
                def f(self) -> int: ...

            class Contract:
                subject @= S

                class renamed:
                    member @= S.f

                    class Clause:
                        """a clause."""
                        kind @= PRE
            ''',
            "t.py": """
            from shikumi_contrace import upholds
            from c import Contract as C

            @upholds(C.renamed.Clause)
            def test_x(): ...
            """,
        }
    )
    findings = [
        f for f in check(test_modules=[project.load("t")]) if f.code == "member-name"
    ]
    assert len(findings) == 1


def test_custom_clause_kinds_are_not_checked_for_position(project):  # CTR_009, VOC_004
    project.write(
        {
            "c.py": '''
            from typing import Protocol
            from shikumi_contrace import define, kind, subject

            class S(Protocol):
                def f(self) -> int: ...

            perf = define.kind("performance")

            class Contract:
                subject @= S

                class Anywhere:
                    """custom kind, any place."""
                    kind @= perf
            ''',
            "t.py": """
            from shikumi_contrace import upholds
            from c import Contract as C

            @upholds(C.Anywhere)
            def test_x(): ...
            """,
        }
    )
    assert [
        f for f in check(test_modules=[project.load("t")]) if f.code == "position"
    ] == []


def test_a_related_test_without_a_binding_is_reported(project):  # REG_010
    project.write(
        {
            "c.py": '''
            from typing import Protocol
            from shikumi_contrace import PRE, kind, member, subject

            class S(Protocol):
                def f(self) -> int: ...

            class Contract:
                subject @= S
                class f:
                    member @= S.f
                    class Clause:
                        """a clause."""
                        kind @= PRE
            ''',
            "t.py": """
            from shikumi_contrace import upholds
            from c import Contract as C

            @upholds(C.f.Clause)
            def test_unbound(): ...
            """,
        }
    )
    assert codes(check(test_modules=[project.load("t")])) == ["unbound"]


def test_a_binding_to_a_parametrized_generic_subject_matches_the_contract(project):
    # SYN_027, REG_010: the binding records the class, so the contract's
    # `subject @= Store` and the test's `binds[Store[Door]]` are the same subject.
    project.write(
        {
            "c.py": '''
            from typing import Protocol, TypeVar
            from shikumi_contrace import PRE, kind, member, subject

            H = TypeVar("H")

            class Store(Protocol[H]):
                def open(self) -> H: ...
                def close(self, handle: H) -> None: ...

            class Contract:
                subject @= Store
                class close:
                    member @= Store.close
                    class Clause:
                        """a clause."""
                        kind @= PRE
            ''',
            "t.py": """
            from shikumi_contrace import binds, upholds
            from c import Store, Contract as C

            class Door: ...

            class Impl:
                def open(self) -> Door: ...
                def close(self, handle: Door) -> None: ...

            @binds[Store[Door]](Impl)
            class Tests:
                @upholds(C.close.Clause)
                def test_x(self): ...
            """,
        }
    )

    assert check(test_modules=[project.load("t")]) == []


def test_a_binding_to_a_different_subject_type_is_reported(project):  # REG_010
    project.write(
        {
            "c.py": '''
            from typing import Protocol
            from shikumi_contrace import PRE, kind, member, subject

            class S(Protocol):
                def f(self) -> int: ...

            class Other(Protocol):
                def g(self) -> int: ...

            class Contract:
                subject @= S
                class f:
                    member @= S.f
                    class Clause:
                        """a clause."""
                        kind @= PRE

            class OtherContract:
                subject @= Other
            ''',
            "t.py": """
            from shikumi_contrace import binds, upholds
            from c import Other, Contract as C

            class Impl:
                def g(self) -> int: ...

            @binds[Other](Impl)
            class Tests:
                @upholds(C.f.Clause)
                def test_x(self): ...
            """,
        }
    )
    assert codes(check(test_modules=[project.load("t")])) == ["binding-mismatch"]


def test_violates_with_a_post_or_inv_clause_is_an_unusual_combination(
    project,
):  # REG_019
    project.write(
        {
            "c.py": '''
            from typing import Protocol
            from shikumi_contrace import INV, POST, kind, member, subject

            class S(Protocol):
                def f(self) -> int: ...

            class Contract:
                subject @= S
                class f:
                    member @= S.f
                    class Post:
                        """a post condition."""
                        kind @= POST
                class Inv:
                    """an invariant."""
                    kind @= INV
            ''',
            "t.py": """
            from shikumi_contrace import binds, violates
            from c import S, Contract as C

            class Impl:
                def f(self) -> int: ...

            @binds[S](Impl)
            class Tests:
                @violates(C.f.Post, C.Inv)
                def test_x(self): ...
            """,
        }
    )
    assert codes(check(test_modules=[project.load("t")])) == [
        "unusual-combination",
        "unusual-combination",
    ]


def test_custom_relation_words_are_not_reported(project):  # VOC_004
    project.write(
        {
            "c.py": '''
            from typing import Protocol
            from shikumi_contrace import POST, kind, member, subject

            class S(Protocol):
                def f(self) -> int: ...

            class Contract:
                subject @= S
                class f:
                    member @= S.f
                    class Post:
                        """a post condition."""
                        kind @= POST
            ''',
            "t.py": """
            from shikumi_contrace import binds, define
            from c import S, Contract as C

            quarantines = define.relation("quarantines")

            class Impl:
                def f(self) -> int: ...

            @binds[S](Impl)
            class Tests:
                @quarantines(C.f.Post)
                def test_x(self): ...
            """,
        }
    )
    assert check(test_modules=[project.load("t")]) == []


def test_check_reports_only_and_changes_nothing(tree):  # REG_006
    (tree.root / "myproj/contracts/user.py").write_text(
        LEAKY_CONTRACT, encoding="utf-8"
    )
    before = (tree.root / "myproj/contracts/user.py").read_text(encoding="utf-8")
    module = tree.load("tests_pkg.test_user")
    first = check(test_modules=[module])
    second = check(test_modules=[module])
    assert first == second
    assert (tree.root / "myproj/contracts/user.py").read_text(
        encoding="utf-8"
    ) == before


def test_the_warning_category_is_a_user_warning():
    assert issubclass(ContraceWarning, UserWarning)


def test_a_contract_dependency_is_included_in_the_derived_contract_range(
    project,
):  # REG_012
    project.write(
        {
            "base.py": """
            from typing import Protocol
            from shikumi_contrace import subject

            class BaseSubject(Protocol): ...

            class BaseContract:
                subject @= BaseSubject
            """,
            "feature.py": """
            from typing import Protocol
            from base import BaseContract
            from shikumi_contrace import PRE, depends_on, kind, member, subject

            class Feature(Protocol):
                def run(self) -> None: ...

            class FeatureContract:
                subject @= Feature
                depends_on @= BaseContract
                class run:
                    member @= Feature.run
                    class Works:
                        'run works.'
                        kind @= PRE
            """,
            "impl.py": """
            class FeatureImpl:
                def run(self) -> None: ...
            """,
            "t.py": """
            from shikumi_contrace import binds, upholds
            from feature import Feature, FeatureContract as C
            from impl import FeatureImpl

            @binds[Feature](FeatureImpl)
            @upholds(C.run.Works)
            def test_x(): ...
            """,
        }
    )
    module = project.load("t")
    assert check(test_modules=[module]) == []


def test_depends_on_outside_a_contract_is_reported(project):  # REG_020
    project.write(
        {
            "c_dep_position.py": """
            from typing import Protocol
            from shikumi_contrace import depends_on, subject

            class S(Protocol): ...
            class Base:
                subject @= S

            class NotAContract:
                depends_on @= Base
            """
        }
    )
    findings = check(contract_assets=["c_dep_position"])
    assert codes(findings) == ["dependency-position"]


def test_depends_on_a_non_contract_class_is_reported(project):  # REG_020
    project.write(
        {
            "c_dep_target.py": """
            from typing import Protocol
            from shikumi_contrace import depends_on, subject

            class S(Protocol): ...
            class NotAContract: ...

            class Contract:
                subject @= S
                depends_on @= NotAContract
            """
        }
    )
    findings = check(contract_assets=["c_dep_target"])
    assert codes(findings) == ["dependency-target"]


def test_a_contract_dependency_cycle_is_reported(project):  # REG_020
    project.write(
        {
            "c_dep_cycle.py": """
            from typing import Protocol
            from shikumi_contrace import subject
            from shikumi_contrace._model import DEPENDENCY, attach

            class S(Protocol): ...
            class A:
                subject @= S
            class B:
                subject @= S

            # The public depends_on syntax only accepts already-existing class
            # objects, so create a pathological runtime state through the
            # internal low-level hook to exercise the validator.
            attach(A, DEPENDENCY, B)
            attach(B, DEPENDENCY, A)
            """
        }
    )
    findings = check(contract_assets=["c_dep_cycle"])
    cycles = [finding for finding in findings if finding.code == "dependency-cycle"]
    assert len(cycles) == 1
    assert "A" in cycles[0].message and "B" in cycles[0].message


def test_on_violation_outside_a_pre_clause_is_reported(project):  # REG_021
    project.write(
        {
            "c_violation_position.py": """
            from typing import Protocol
            from shikumi_contrace import POST, REJECTED, kind, member, on_violation, subject

            class S(Protocol):
                def f(self) -> int: ...

            class Contract:
                subject @= S
                class f:
                    member @= S.f
                    class After:
                        'a postcondition.'
                        kind @= POST
                        on_violation @= REJECTED
            """
        }
    )
    findings = check(contract_assets=["c_violation_position"])
    assert codes(findings) == ["violation-position"]


def test_on_violation_does_not_require_or_forbid_test_shapes(project):  # AIM_016
    project.write(
        {
            "c_violation_meaning.py": """
            from typing import Protocol
            from shikumi_contrace import OUT_OF_SCOPE, PRE, REJECTED, kind, member, on_violation, subject

            class S(Protocol):
                def f(self, value: int) -> int: ...

            class Contract:
                subject @= S
                class f:
                    member @= S.f
                    class Rejected:
                        'negative values are invalid.'
                        kind @= PRE
                        on_violation @= REJECTED
                    class Outside:
                        'large values are outside the contract.'
                        kind @= PRE
                        on_violation @= OUT_OF_SCOPE
            """,
            "impl_violation_meaning.py": """
            class Impl:
                def f(self, value: int) -> int:
                    return value
            """,
            "t_violation_meaning.py": """
            from shikumi_contrace import binds, upholds, violates
            from c_violation_meaning import S, Contract as C
            from impl_violation_meaning import Impl

            @binds[S](Impl)
            class Tests:
                @upholds(C.f.Rejected)
                def test_rejected_clause_has_no_special_test_shape(self): ...

                @violates(C.f.Outside)
                def test_out_of_scope_clause_may_still_be_observed(self): ...
            """,
        }
    )
    findings = check(test_modules=[project.load("t_violation_meaning")])
    assert findings == []
