# shikumi-contrace

`shikumi-contrace` is a library for describing contracts about software behavior as referenceable Python assets.

Keeping contracts separate from implementations and tests makes the following information explicit.

- What is the subject of a contract
- What behavior is promised
- Which tests address which clauses
- Which implementation corresponds to which contract subject
- What dependencies exist between contracts

```text
contract
   ↑
   │ upholds / violates
   │
 test ───── binds ───── implementation
```

Contracts are written as ordinary Python code and can be referenced by people, LLMs, and tools.

`shikumi-contrace` is not a library that generates tests from contracts. Tests are written normally, with declarations that state which contracts they address.

## Installation

The current version is `0.1.0`.

```bash
pip install shikumi-contrace
```

To use the pytest integration:

```bash
pip install "shikumi-contrace[pytest]"
```

## Example

### Boundary types

```python
# contract/ports/reservation.py

from dataclasses import dataclass


@dataclass(frozen=True)
class Reservation:
    sku: str
    quantity: int
```

```python
# contract/inventory.py

from typing import Protocol

from .ports.reservation import Reservation


class Inventory(Protocol):
    def reserve(self, sku: str, quantity: int) -> Reservation: ...
```

### Contract

```python
# contract/inventory_contract.py

from shikumi_contrace import (
    INV,
    POST,
    PRE,
    REJECTED,
    kind,
    member,
    on_violation,
    subject,
)

from .inventory import Inventory


class InventoryContract:
    subject @= Inventory

    class StockUnchangedOnFailure:
        """A failed reservation does not change stock."""

        kind @= INV

    class reserve:
        member @= Inventory.reserve

        class QuantityMustBePositive:
            """Reservation quantity must be greater than zero."""

            kind @= PRE
            on_violation @= REJECTED

        class ReservationIsReturned:
            """A successful reservation returns a reservation handle."""

            kind @= POST
```

### Implementation

```python
# inventory_service.py

from contract.ports.reservation import Reservation


class InventoryService:
    def __init__(self, stock: dict[str, int]) -> None:
        self.stock = dict(stock)

    def reserve(self, sku: str, quantity: int) -> Reservation:
        if quantity <= 0:
            raise ValueError("quantity must be positive")

        available = self.stock.get(sku, 0)

        if quantity > available:
            raise ValueError("insufficient stock")

        self.stock[sku] = available - quantity

        return Reservation(
            sku=sku,
            quantity=quantity,
        )
```

### Tests

```python
# test_inventory.py

import pytest

from shikumi_contrace import (
    Phase,
    binds,
    upholds,
    violates,
)

from contract.inventory import Inventory
from contract.inventory_contract import InventoryContract as Contract
from inventory_service import InventoryService


@binds[Inventory](InventoryService)
class TestReserve:
    @upholds(Contract.reserve.ReservationIsReturned)
    def test_returns_reservation(self):
        with Phase.PREPARE:
            inventory = InventoryService(
                stock={"book": 10},
            )

        with Phase.MAIN:
            reservation = inventory.reserve(
                "book",
                2,
            )

        with Phase.VERIFY:
            assert reservation.sku == "book"
            assert reservation.quantity == 2

    @violates(Contract.reserve.QuantityMustBePositive)
    @upholds(Contract.StockUnchangedOnFailure)
    def test_rejects_zero_quantity(self):
        with Phase.PREPARE:
            inventory = InventoryService(
                stock={"book": 10},
            )
            before = dict(inventory.stock)

        with Phase.MAIN:
            with pytest.raises(ValueError):
                inventory.reserve(
                    "book",
                    0,
                )

        with Phase.VERIFY:
            assert inventory.stock == before
```

## Vocabulary

### Contract declarations

| Vocabulary | Use | Example |
|---|---|---|
| `subject` | Specify the contract subject | `subject @= Inventory` |
| `member` | Specify a member of the subject | `member @= Inventory.reserve` |
| `kind` | Specify the kind of a clause | `kind @= PRE` |
| `on_violation` | Describe the handling of a PRE violation | `on_violation @= REJECTED` |
| `depends_on` | Describe a dependency on another contract asset | `depends_on @= OtherClause` |

### Clause kinds

| Vocabulary | Meaning |
|---|---|
| `PRE` | A condition that holds before an operation |
| `POST` | A condition that holds after an operation |
| `INV` | A condition maintained across operations |

### Violation handling

| Vocabulary | Meaning |
|---|---|
| `REJECTED` | A violating call is not accepted as a normal success |
| `OUT_OF_SCOPE` | Behavior on violation is outside the promise of that clause |

`REJECTED` does not prescribe how rejection is represented. An exception, result type, HTTP response, or another implementation-appropriate form can be used.

`OUT_OF_SCOPE` means that the clause makes no promise about behavior when the condition is violated.

These words do not build a complete trust-boundary model, but they can be used to express concisely how far a condition is trusted and how far behavior on violation is included in the contract.

### Test relations

| Vocabulary | Use |
|---|---|
| `@upholds(...)` | The test addresses behavior that satisfies a clause |
| `@violates(...)` | The test addresses a violation of a clause |
| `@binds[Subject](Implementation)` | Record the correspondence between a subject and an implementation |

`Phase` is re-exported as an alias of `metamk.Mk`.

```python
with Phase.PREPARE:
    ...

with Phase.MAIN:
    ...

with Phase.VERIFY:
    ...
```

## Contract dependencies

Dependencies between contracts can be expressed with `depends_on`.

```python
class ReservationCanBeCancelled:
    depends_on @= InventoryContract.reserve.ReservationIsReturned
```

In this case, a change or retirement of `ReservationIsReturned` also makes `ReservationCanBeCancelled` something to re-evaluate.

Multiple dependencies can be declared.

```python
class Something:
    depends_on @= ContractA
    depends_on @= ContractB
```

Dependencies are treated as an acyclic structure.

## Generic subjects

A generic Protocol can also be used as a subject.

```python
from typing import Protocol, TypeVar

T = TypeVar("T")


class Repository(Protocol[T]):
    def get(self, key: str) -> T: ...
```

```python
@binds[Repository[User]](UserRepository)
class TestUserRepository: ...
```

The type checker uses `Repository[User]`, while at runtime the origin `Repository` is used as the subject identity.

## Contract assets and ports

A contract can consist of multiple modules.

```text
contract/
├── __init__.py
├── inventory.py
├── inventory_contract.py
└── ports/
    ├── __init__.py
    └── reservation.py
```

Types that cross the contract boundary are placed under `ports/`.

| Kind | Use |
|---|---|
| dataclass | Data that crosses the boundary |
| Protocol | Behavior at the boundary |
| enum | Values shared by the contract |
| type alias | Type expressions used by the contract |

Keeping contract and ports together lets the types needed by the contract remain part of the same asset when the implementation is replaced.

## Open vocabulary

Custom vocabulary can be defined in addition to the standard vocabulary.

```python
CUSTOM = define.kind("custom")
```

Custom vocabulary can also be added for violation handling.

```python
CUSTOM_POLICY = define.violation("custom")
```

The standard vocabulary provides common contract expressions, while domain-specific expressions can be added as needed.

## Reading contract information

Information recorded on contracts can be read at runtime.

```python
clauses = clauses_of(InventoryContract)
```

Clauses without a recorded test relation can also be retrieved.

```python
missing = untested_clauses(InventoryContract)
```

`untested_clauses()` returns clauses for which contrace has no recorded test relation.

It does not decide whether a test is required from the clause kind or the value of `on_violation`.

## Validation

Structural issues in contract assets and relations can be validated.

- contract structure
- placement of `ports`
- cycles in contract dependency
- placement of metadata

Validation returns diagnostics for declared structures and relations.

Design meaning and validity can be judged by people, LLMs, and other tooling from the information recorded in the contract.

## pytest integration

pytest integration is optional.

```python
pytest_plugins = [
    "shikumi_contrace.pytest",
]
```

With the plugin enabled, pytest can use contract relations for display and validation.

```bash
pytest --contrace-check
```

Normal pytest features such as fixtures, parametrize, and markers remain available.

## Documentation

This README introduces the basic usage and main concepts.

For detailed semantics, structural rules, and validation behavior, see the following documents.

- [Specification](https://github.com/minoru-jp/shikumi-contrace/blob/main/docs/specification/INDEX.md)
- [Architecture](https://github.com/minoru-jp/shikumi-contrace/blob/main/docs/specification/aim.md)
- [Glossary](https://github.com/minoru-jp/shikumi-contrace/blob/main/docs/glossary.md)
- [API reference](https://github.com/minoru-jp/shikumi-contrace/blob/main/docs/specification/api.md)
- [pytest integration](https://github.com/minoru-jp/shikumi-contrace/blob/main/docs/specification/pytest_integration.md)

## License

MIT License. See `LICENSE` for details.
