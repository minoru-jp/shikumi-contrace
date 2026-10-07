"""The boundary types: the ``ports`` package (IND_010-IND_015, REG_012, REG_023-REG_028).

The layout under test is ``shop/contract/`` (the contract asset, any name) with
``ports/`` directly inside it::

    shop/
      contract/
        order.py          the contract and its subject type
        ports/
          shapes.py       Protocols and data
      implementation.py
"""

from __future__ import annotations

import importlib

from shikumi_contrace.checking import CONTRACT_ASSET_STRUCTURE, Diagnostic, check

SHAPES = """
from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple, Protocol, TypedDict


class Reservation(Protocol):
    @property
    def sku(self) -> str: ...


@dataclass(frozen=True)
class Receipt:
    amount_cents: int


class Color(Enum):
    RED = 1


class Pair(NamedTuple):
    left: int
    right: int


class Doc(TypedDict):
    title: str


Handle = int
"""

CONTRACT = '''
from typing import Protocol

from shikumi_contrace import POST, kind, member, subject
from shop.contract.ports.shapes import Reservation


class Service(Protocol):
    def reserve(self, sku: str) -> Reservation: ...


class ServiceContract:
    subject @= Service

    class reserve:
        member @= Service.reserve

        class Returns:
            """It returns a reservation."""

            kind @= POST
'''

IMPL = """
class Impl:
    def reserve(self, sku: str) -> object: ...
"""

TESTS = """
from shikumi_contrace import binds, upholds
from shop.contract.order import Service
from shop.contract.order import ServiceContract as C
from shop.implementation import Impl


@binds[Service](Impl)
class Tests:
    @upholds(C.reserve.Returns)
    def test_it(self): ...
"""


def files(changes: dict[str, str] | None = None) -> dict[str, str]:
    base = {
        "shop/contract/ports/shapes.py": SHAPES,
        "shop/contract/order.py": CONTRACT,
        "shop/implementation.py": IMPL,
        "t.py": TESTS,
    }
    base.update(changes or {})
    return base


def codes(findings: list[Diagnostic]) -> list[str]:
    return [finding.code for finding in findings]


def derived(project, changes: dict[str, str] | None = None) -> list[Diagnostic]:
    project.write(files(changes))
    return check(test_modules=[project.load("t")])


def declared(
    project, assets: list[str], changes: dict[str, str] | None = None
) -> list[Diagnostic]:
    project.write(files(changes))
    _ = project.load("t")
    return check(
        contract_assets=assets, tests=["t"], implementations=["shop.implementation"]
    )


# --- the layout, and what a name may be ----------------------------------------
def test_the_layout_is_accepted(project):  # IND_010
    assert derived(project) == []


def test_the_package_that_holds_the_contracts_can_have_any_name(project):  # IND_010
    project.write(
        {
            "agreements/ports/shapes.py": SHAPES,
            "agreements/order.py": CONTRACT.replace("shop.contract", "agreements"),
            "shop/implementation.py": IMPL,
            "t.py": TESTS.replace("shop.contract", "agreements"),
        }
    )

    assert check(test_modules=[project.load("t")]) == []


def test_contracts_may_live_in_sub_packages_of_the_contract_asset(project):  # IND_010
    # A large contract asset: the contracts are in sub-packages, `ports` is above them.
    project.write(
        {
            "shop/contract/billing/invoice.py": CONTRACT,
            "shop/contract/ports/shapes.py": SHAPES,
            "shop/implementation.py": IMPL,
            "t.py": TESTS.replace(
                "shop.contract.order", "shop.contract.billing.invoice"
            ),
        }
    )

    assert check(test_modules=[project.load("t")]) == []


def test_the_structure_specification_is_usable_with_shikumi_itself(project):  # REG_027
    from shikumi import Shikumi
    from shikumi.standard import PackageTreeStructure

    project.write(files())
    package = importlib.import_module("shop.contract")

    result = Shikumi(structure=PackageTreeStructure()).validate(
        package, structure_specification=CONTRACT_ASSET_STRUCTURE
    )

    assert result.is_valid


# --- derivation ------------------------------------------------------------------
def test_the_boundary_types_a_contract_refers_to_join_the_range(project):  # REG_012
    # The contract refers to shop.contract.ports, so it is checked for what a
    # contract asset must not refer to (IND_003), without being declared.
    leaky = SHAPES + "\nfrom shop.implementation import Impl as _Impl\n"

    assert codes(derived(project, {"shop/contract/ports/shapes.py": leaky})) == [
        "independence"
    ]


def test_an_external_package_named_ports_is_not_derived_as_boundary_types(
    project,
):  # REG_012
    external = """
class ExternalThing:
    def run(self) -> int:
        return 1
"""
    contract = CONTRACT.replace(
        "from shop.contract.ports.shapes import Reservation",
        "from vendor.ports.types import ExternalThing\n"
        "from shop.contract.ports.shapes import Reservation",
    )

    assert (
        derived(
            project,
            {
                "vendor/ports/types.py": external,
                "shop/contract/order.py": contract,
            },
        )
        == []
    )


def test_an_external_package_named_ports_is_not_an_undeclared_boundary_type(
    project,
):  # REG_025
    external = "class ExternalThing: ...\n"
    contract = CONTRACT.replace(
        "from shop.contract.ports.shapes import Reservation",
        "from vendor.ports.types import ExternalThing\n"
        "from shop.contract.ports.shapes import Reservation",
    )

    assert (
        declared(
            project,
            ["shop.contract"],
            {
                "vendor/ports/types.py": external,
                "shop/contract/order.py": contract,
            },
        )
        == []
    )


# --- structure: checked by Shikumi -----------------------------------------------
def test_ports_has_to_be_a_package(project):  # IND_010, REG_027
    project.write(
        {
            "shop/contract/ports.py": SHAPES,
            "shop/contract/order.py": CONTRACT.replace(
                "shop.contract.ports.shapes", "shop.contract.ports"
            ),
            "shop/implementation.py": IMPL,
            "t.py": TESTS,
        }
    )

    found = check(test_modules=[project.load("t")])

    assert codes(found) == ["ports-structure"]
    assert "expected package, got module" in found[0].message


def test_ports_holds_modules_and_no_sub_package(project):  # IND_010, REG_027
    found = derived(
        project, {"shop/contract/ports/sub/deep.py": "from typing import Protocol\n"}
    )

    assert codes(found) == ["ports-structure"]
    assert "ports.sub" in found[0].message


# --- placement: the package that holds ports is a contract asset -------------------
def test_ports_next_to_the_implementation_is_reported(project):  # IND_015, REG_028
    # `shop` holds the implementation, so it is not a contract asset.
    project.write(
        {
            "shop/ports/shapes.py": SHAPES,
            "shop/contract/order.py": CONTRACT.replace(
                "shop.contract.ports.shapes", "shop.ports.shapes"
            ),
            "shop/implementation.py": IMPL,
            "t.py": TESTS,
        }
    )

    found = check(test_modules=[project.load("t")])

    assert codes(found) == ["ports-placement"]
    assert found[0].subject == "shop"
    assert "shop.implementation" in found[0].message


def test_a_test_inside_the_contract_asset_is_reported_too(project):  # IND_015, REG_028
    project.write(
        {
            "shop/contract/ports/shapes.py": SHAPES,
            "shop/contract/order.py": CONTRACT,
            "shop/implementation.py": IMPL,
            "shop/contract/t_inside.py": TESTS,
        }
    )

    found = check(test_modules=[project.load("shop.contract.t_inside")])

    assert "ports-placement" in codes(found)


def test_ports_at_the_top_level_is_reported(project):  # IND_010, REG_028
    project.write(
        {
            "ports/shapes.py": SHAPES,
            "contract/order.py": CONTRACT.replace(
                "shop.contract.ports.shapes", "ports.shapes"
            ),
            "shop/implementation.py": IMPL,
            "t.py": TESTS.replace("shop.contract.order", "contract.order"),
        }
    )

    assert codes(check(test_modules=[project.load("t")])) == ["ports-placement"]


# --- content of ports -------------------------------------------------------------
def test_a_contract_does_not_belong_in_the_boundary_types(project):  # REG_023
    inside = SHAPES + (
        "\nfrom shikumi_contrace import subject\n\n"
        "class Inner:\n"
        "    subject @= Reservation\n"
    )

    found = derived(project, {"shop/contract/ports/shapes.py": inside})

    assert "ports-contract" in codes(found)


def test_the_boundary_types_hold_no_behavior(project):  # REG_023
    behaving = SHAPES + (
        "\ndef total(receipts):\n    return sum(r.amount_cents for r in receipts)\n"
        "\nclass Helper:\n    def run(self) -> int:\n        return 1\n"
    )

    found = derived(project, {"shop/contract/ports/shapes.py": behaving})

    assert codes(found) == ["ports-behavior", "ports-behavior"]
    assert {f.subject for f in found} == {
        "shop.contract.ports.shapes.total",
        "shop.contract.ports.shapes.Helper",
    }


def test_the_init_of_ports_holds_no_definitions(project):  # IND_012, REG_023
    found = derived(
        project,
        {
            "shop/contract/ports/__init__.py": "class Shape:\n    pass\n\ndef helper(): ...\n"
        },
    )

    assert codes(found) == ["ports-definition-in-init", "ports-definition-in-init"]


def test_the_init_of_ports_may_reexport(project):  # IND_012
    reexport = "from shop.contract.ports.shapes import Receipt, Reservation\n"

    assert derived(project, {"shop/contract/ports/__init__.py": reexport}) == []


# --- references and the parents ---------------------------------------------------
def test_the_boundary_types_do_not_refer_to_shikumi_contrace(project):  # REG_024
    found = derived(
        project,
        {
            "shop/contract/ports/shapes.py": SHAPES
            + "\nfrom shikumi_contrace import note\n"
        },
    )

    assert codes(found) == ["ports-reference"]


def test_the_boundary_types_do_not_refer_to_a_contract(project):  # REG_024
    project.write(
        {
            "shop/contract/other.py": CONTRACT.replace(
                "from shop.contract.ports.shapes import Reservation", ""
            ).replace("-> Reservation", "-> int"),
            "shop/contract/ports/shapes.py": SHAPES
            + "\nfrom shop.contract.other import ServiceContract as _C\n",
            "shop/contract/order.py": CONTRACT,
            "shop/implementation.py": IMPL,
            "t.py": TESTS,
        }
    )
    _ = project.load("t")

    found = check(
        contract_assets=["shop.contract"],
        tests=["t"],
        implementations=["shop.implementation"],
    )

    assert codes(found) == ["ports-reference"]


def test_the_init_of_the_contract_asset_must_not_import_a_contract(project):  # REG_024
    # Importing shop.contract.ports runs shop/contract/__init__.py first, which
    # would load the contract (and shikumi-contrace) into whatever imports ports.
    found = derived(
        project, {"shop/contract/__init__.py": "from shop.contract import order\n"}
    )

    assert codes(found) == ["ports-parent"]
    assert found[0].subject == "shop.contract"


def test_a_relative_import_in_the_init_is_reported_too(project):  # REG_024
    found = derived(project, {"shop/contract/__init__.py": "from . import order\n"})

    assert codes(found) == ["ports-parent"]


def test_an_empty_init_of_the_contract_asset_is_what_is_expected(project):  # REG_024
    assert derived(project, {"shop/contract/__init__.py": ""}) == []


# --- declared ranges --------------------------------------------------------------
def test_declaring_the_contract_asset_includes_its_ports(project):  # REG_014, REG_025
    # One declared root is enough: ports is inside it.
    assert declared(project, ["shop.contract"]) == []


def test_a_boundary_types_package_that_is_not_declared_is_reported(project):  # REG_025
    found = declared(project, ["shop.contract.order"])

    assert codes(found) == ["ports-undeclared"]
    assert "shop.contract.ports" in found[0].message


# --- value shapes live in ports ---------------------------------------------------
def test_a_protocol_that_is_not_a_subject_type_belongs_in_ports(project):  # REG_026
    contract = CONTRACT + (
        "\nclass Reservation2(Protocol):\n"
        "    @property\n"
        "    def sku(self) -> str: ...\n"
    )

    found = derived(project, {"shop/contract/order.py": contract})

    assert codes(found) == ["shape-outside-ports"]
    assert found[0].subject == "shop.contract.order.Reservation2"


def test_subject_types_and_data_stay_in_the_contract_module(project):  # REG_026
    contract = CONTRACT + (
        "\nfrom dataclasses import dataclass\n\n@dataclass\nclass Row:\n    sku: str\n"
    )

    assert derived(project, {"shop/contract/order.py": contract}) == []


def test_a_generic_subject_type_is_a_subject_type(project):  # REG_026
    contract = '''
from typing import Protocol, TypeVar

from shikumi_contrace import POST, kind, member, subject
from shop.contract.ports.shapes import Reservation

R = TypeVar("R", bound=Reservation)


class Service(Protocol[R]):
    def reserve(self, sku: str) -> R: ...


class ServiceContract:
    subject @= Service

    class reserve:
        member @= Service.reserve

        class Returns:
            """It returns what release takes."""

            kind @= POST
'''

    assert derived(project, {"shop/contract/order.py": contract}) == []
