<!--
この文書は `shikumi-devdoc` によって生成された canonical document です。
Canonical source は `devdocs/canonical_sources/readme.py` です。
直接編集しないでください。

公開文書作成方針

- `devdocs/canonical_documents/` にある日本語 canonical document を英語へ翻訳し、リポジトリのトップレベルまたは `docs/` に公開文書として配備する。
- 翻訳では意味、構造、情報量を維持し、内容を勝手に追加・削除・要約しない。
- canonical document に `shikumi-devdoc:translation-metadata` が含まれる場合は、その `preserve_spelling` 指定の用語の表記を変更しない。
- コード、Python 識別子、コマンド、ファイルパス、URL は、翻訳上の必要がない限り変更しない。
- このコメントブロックと `shikumi-devdoc:translation-metadata` は published document には含めない。
- published document は canonical document から派生する公開成果物として扱い、内容の変更が必要な場合は canonical source または realization context へ戻して canonical document を再生成する。
-->

# shikumi-contrace

`shikumi-contrace` は、ソフトウェアの振る舞いに関する契約を、Python 上の参照可能な資産として記述するためのライブラリです。

契約を実装やテストから分離しておくことで、次のような情報を明示できます。

- 何を契約対象とするか
- どのような振る舞いを約束するか
- どのテストがどの条項を扱っているか
- どの実装がどの契約対象に対応しているか
- 契約同士にどのような依存があるか

```text
contract
   ↑
   │ upholds / violates
   │
 test ───── binds ───── implementation
```

契約は通常の Python コードとして記述され、人間、LLM、ツールから参照できます。

`shikumi-contrace` は契約からテストを自動生成するライブラリではありません。テストは通常どおり記述し、そのテストがどの契約を扱うかを明示します。

## Installation

現在のバージョンは `0.1.0` です。

```bash
pip install shikumi-contrace
```

pytest 連携を利用する場合:

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

| 語彙 | 用途 | 例 |
|---|---|---|
| `subject` | 契約対象を指定する | `subject @= Inventory` |
| `member` | 対象のメンバーを指定する | `member @= Inventory.reserve` |
| `kind` | 条項の種類を指定する | `kind @= PRE` |
| `on_violation` | PRE 違反時の扱いを記述する | `on_violation @= REJECTED` |
| `depends_on` | 他の契約資産への依存を記述する | `depends_on @= OtherClause` |

### Clause kinds

| 語彙 | 意味 |
|---|---|
| `PRE` | 操作前に成立する条件 |
| `POST` | 操作後に成立する条件 |
| `INV` | 操作をまたいで維持される条件 |

### Violation handling

| 語彙 | 意味 |
|---|---|
| `REJECTED` | 条件違反を正常な成功として受理しない |
| `OUT_OF_SCOPE` | 条件違反時の振る舞いをその条項の契約範囲に含めない |

`REJECTED` は拒否の方法を規定しません。例外、結果型、HTTP response など、実装に応じた方法を利用できます。

`OUT_OF_SCOPE` は、違反時の振る舞いについて契約上の約束を置かないことを表します。

これらの語彙は、完全な信頼境界モデルを構築するものではありませんが、ある条件をどこまで信頼し、違反時の扱いをどこまで契約に含めるかを簡潔に表現するためにも利用できます。

### Test relations

| 語彙 | 用途 |
|---|---|
| `@upholds(...)` | テストが条項を満たす振る舞いを扱う |
| `@violates(...)` | テストが条項違反を扱う |
| `@binds[Subject](Implementation)` | subject と implementation の対応を記録する |

`Phase` は `metamk.Mk` の alias として再エクスポートされます。

```python
with Phase.PREPARE:
    ...

with Phase.MAIN:
    ...

with Phase.VERIFY:
    ...
```

## Contract dependencies

契約同士の依存関係は `depends_on` で表現できます。

```python
class ReservationCanBeCancelled:
    depends_on @= InventoryContract.reserve.ReservationIsReturned
```

この場合、`ReservationIsReturned` の変更や廃止に伴って、`ReservationCanBeCancelled` も再評価の対象になります。

複数の依存先も宣言できます。

```python
class Something:
    depends_on @= ContractA
    depends_on @= ContractB
```

依存関係は循環しない構造として扱われます。

## Generic subjects

generic Protocol も subject として利用できます。

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

型検査では `Repository[User]` が利用され、runtime では origin である `Repository` が subject identity として扱われます。

## Contract assets and ports

契約は複数の module から構成できます。

```text
contract/
├── __init__.py
├── inventory.py
├── inventory_contract.py
└── ports/
    ├── __init__.py
    └── reservation.py
```

`ports/` には、契約の境界を横切る型を配置します。

| 種類 | 用途 |
|---|---|
| dataclass | 境界を横切るデータ |
| Protocol | 境界上の振る舞い |
| enum | 契約で共有する値 |
| type alias | 契約上の型表現 |

contract と ports をまとめて保持することで、implementation を置き換える場合にも契約上必要な型を同じ資産として扱えます。

## Open vocabulary

標準語彙に加えて、独自の語彙を定義できます。

```python
CUSTOM = define.kind("custom")
```

違反時の扱いにも独自語彙を追加できます。

```python
CUSTOM_POLICY = define.violation("custom")
```

標準語彙は共通的な契約表現として提供され、必要に応じてドメイン固有の表現を追加できます。

## Reading contract information

契約に記録された情報は runtime から取得できます。

```python
clauses = clauses_of(InventoryContract)
```

テストとの relation が記録されていない条項も取得できます。

```python
missing = untested_clauses(InventoryContract)
```

`untested_clauses()` は、contrace に記録された test relation が存在しない条項を返します。

条項の種類や `on_violation` の値から、テストの必要性を判断する処理は行いません。

## Validation

contract asset や relation について、構造上確認できる問題を validation できます。

- contract structure
- `ports` の配置
- contract dependency の循環
- metadata の配置

validation は、宣言された構造と関係に対して診断を返します。

設計上の意味や妥当性については、契約に記述された情報をもとに人間や LLM、各種 tooling が判断できます。

## pytest integration

pytest integration は optional です。

```python
pytest_plugins = [
    "shikumi_contrace.pytest",
]
```

plugin を有効にすると、contract relation を利用した表示や validation を pytest から利用できます。

```bash
pytest --contrace-check
```

fixture、parametrize、marker など、通常の pytest 機能も利用できます。

## Documentation

README では基本的な使い方と主要な概念を紹介しています。

詳細な意味論、構造規則、validation behavior については各文書を参照してください。

- [Specification](https://github.com/minoru-jp/shikumi-contrace/blob/main/docs/specification/INDEX.md)
- [Architecture](https://github.com/minoru-jp/shikumi-contrace/blob/main/docs/specification/aim.md)
- [Glossary](https://github.com/minoru-jp/shikumi-contrace/blob/main/docs/glossary.md)
- [API reference](https://github.com/minoru-jp/shikumi-contrace/blob/main/docs/specification/api.md)
- [pytest integration](https://github.com/minoru-jp/shikumi-contrace/blob/main/docs/specification/pytest_integration.md)

## License

MIT License です。詳細は `LICENSE` を参照してください。
