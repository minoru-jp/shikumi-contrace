<!--
この文書は `shikumi-devdoc` によって生成された canonical document です。
Canonical source は `devdocs/canonical_sources/specification/__init__.py` です。
直接編集しないでください。

公開文書作成方針

- `devdocs/canonical_documents/` にある日本語 canonical document を英語へ翻訳し、リポジトリのトップレベルまたは `docs/` に公開文書として配備する。
- 翻訳では意味、構造、情報量を維持し、内容を勝手に追加・削除・要約しない。
- canonical document に `shikumi-devdoc:translation-metadata` が含まれる場合は、その `preserve_spelling` 指定の用語の表記を変更しない。
- コード、Python 識別子、コマンド、ファイルパス、URL は、翻訳上の必要がない限り変更しない。
- このコメントブロックと `shikumi-devdoc:translation-metadata` は published document には含めない。
- published document は canonical document から派生する公開成果物として扱い、内容の変更が必要な場合は canonical source または realization context へ戻して canonical document を再生成する。
-->

# 契約の独立性

設計や実装がスクラッチで作り直しになったときに、契約だけを独立した資産として持ち出せるようにするための規則を定める。契約とテストの密結合を、構造として防ぐ。

## IND_001

契約は、テストおよび実装とは別の module または package、すなわち契約資産に置かなければならない。契約の規模が小さい場合も同様である。

title: Contracts live in a separate contract asset

level: MUST

detail: 設計・実装がある程度進んだ後で、行き詰まりやスクラッチでの作り直しの判断が出たときに、契約だけを独立した資産として持ち出せるようにするため。

related: [CTR_001](contract.md#ctr_001)

## IND_002

契約資産は、テストへの参照を持ってはならない。module、クラス、関数、値のいずれの形であっても同様である。

title: A contract asset does not refer to tests

level: MUST NOT

detail: 契約がテストを参照できないことを、構造として規定することで、契約とテストの密結合を防ぐ。契約からテストへの対応は、テストの側が関係づけとして持つ。

## IND_003

契約資産は、実装への参照を持ってはならない。module、クラス、関数、値のいずれの形であっても同様である。

title: A contract asset does not refer to implementations

level: MUST NOT

detail: 実装がスクラッチで失われたとき、契約が import できなくなることを防ぐ。契約は、実装の型の代わりに、契約自身が定義する構造的な型を用いる。

related: [CTR_003](contract.md#ctr_003)

## IND_004

契約資産は、契約を持ち出した先で読み込めるように、実行時の依存を少なくすることが望ましい。契約資産が import する shikumi-contrace の部分は、本体に留めることが望ましい。shikumi-contrace は、この指針を強制しない。

title: Guidance: keep the runtime dependencies of a contract asset small

level: INFORMATIVE

detail: 契約を持ち出した先に、依存するライブラリがなければ、契約を読み込めない。第三者ライブラリの型は、型注釈の中にだけ現れる書き方で、実行時の import を避けられる。具体的には、型注釈の評価を遅らせ（`from __future__ import annotations`）、型の import を `if TYPE_CHECKING:` の中に置く。この書き方でも、型チェッカーは実際の型を検査できる。ただし、型を検査するには、そのライブラリが型チェッカーから見える環境にある必要がある。

## IND_005

shikumi-contrace は、実装が契約または shikumi-contrace を import すること、契約の型を継承すること、その他の実装の書き方を制約する要求をしてはならない。

title: Contracts do not shape the implementation

level: MUST NOT

detail: 契約は、テストに用いるための概念に留める。契約の存在が、実装の設計に影響を与えてはならない。

related: [AIM_001](aim.md#aim_001)

## IND_006

実装は、対象型に、構造的部分型によって適合しなければならない。名前による継承ではない。

title: Conformance is structural

level: MUST

related: [CTR_003](contract.md#ctr_003)

## IND_007

契約の対象型と実装を結び付ける束縛は、テストの側に置かなければならない。

title: Binding is held by the test side

level: MUST

detail: 契約と実装は互いを知らないため、両者を知ることができるのはテストだけである。

## IND_008

依存の向きは次のとおりである。テストは契約と実装の両方に依存し、契約と実装は互いを知らない。

```text
test ──▶ contract asset
  └─────▶ implementation

contract asset ──▶ (depends on neither tests nor implementations)
```

title: Direction of dependencies

level: INFORMATIVE

## IND_009

shikumi-contrace は、契約資産が、テストおよび実装以外のものに依存することを、制限してはならない。

title: Dependencies other than tests and implementations are not restricted

level: MUST NOT

detail: 制限するのは、利用者が宣言したパッケージの境界（契約資産から、テストと実装への参照）に限る。それ以外の依存を制限すると、すべてのユースケースを想定できない以上、利用者にとって思わぬ落とし穴になる。標準ライブラリか第三者ライブラリかといった分類も、制限の根拠にしない。

## IND_010

契約と実装が共有する値の形、すなわち境界の型は、`ports` という名前のパッケージに置かなければならない。`ports` は、契約資産のパッケージの直下に置く。契約資産のパッケージの名前は、任意である。

title: Boundary types live in a package named ports, directly inside the contract asset

level: MUST

related: [CTR_003](contract.md#ctr_003)

detail: 対象型のメソッドの引数は反変であり、実装が自前の具象クラスでそれを受けると、契約が約束した範囲を受けきれず、型チェッカーに拒否される。実装が同じ形を自前の Protocol で二重に書く代わりに、境界の型を共有する。配置は、`contract/`（契約資産。名前は任意）の直下に、`ports/` パッケージを置き、Protocol とデータを `ports/` の中のモジュールに書く形である。パッケージに限るのは、規模が小さいうちも大きくなってからも、同じ構造のままにするためである。名前を `ports` に固定するのは、導出と検査が、設定なしに境界の型を見つけられるようにするためである（REG_012、REG_027）。契約資産のパッケージの直下に置くのは、契約を持ち出すときに、ディレクトリ一つで運べるようにし、範囲の宣言も一つのルートで済ませるためである。契約を先に書いて実装を作る使い方を想定した規定であり、実装が `ports` から import するかどうかは、実装の自由である（IND_005）。

## IND_011

契約の module は、どの契約の対象型でもない Protocol を定義してはならない。値の形は `ports` に置く。

title: A contract module defines no Protocol other than subject types

level: MUST NOT

related: [CTR_003](contract.md#ctr_003)

detail: 契約の module に置いてよい Protocol は、契約の対象型だけである。総称型の対象型（`Inventory[R]` のようなもの）も、対象型である。メソッドの引数や戻り値に現れる値の形（`Reservation`、`Order` など）は、対象型ではないので、`ports` に置く。検出するのは Protocol だけで、dataclass などのデータの型を契約の module に置いたことは、検出しない。

## IND_012

`ports` の中のモジュールが定義してよいのは、Protocol とデータ（dataclass、NamedTuple、TypedDict、Enum）に限る。型の別名、型変数、定数は置いてよい。契約、関数、これら以外のクラスは、定義してはならない。`ports` 自身の `__init__` は、定義を持たず、中のモジュールの再公開だけを書いてよい。

title: The boundary types hold only Protocols and data, defined in modules

level: MUST

related: [CTR_003](contract.md#ctr_003)

detail: 境界の型は、形を共有するためのものであり、ふるまいを持たない。dataclass が持つメソッドは、データの型の一部として許す。例外クラスなど、ここに挙げた以外のクラスは、実装の側または契約の外に置く。`__init__` に定義を置かないのは、定義の置き場所を一つにそろえ、読み手が `ports` の中身を、モジュールを辿って探せるようにするためである。

## IND_013

`ports` は、契約、shikumi-contrace、テスト、実装を参照してはならない。`ports` を import する経路にある親パッケージの `__init__`（契約資産のパッケージの `__init__` を含む）は、契約と shikumi-contrace を import してはならない。

title: The boundary types refer to no contract, no shikumi-contrace, no test and no implementation

level: MUST NOT

detail: テストと実装への参照は、契約資産の規則（IND_002、IND_003）がそのまま及ぶ。契約と shikumi-contrace への参照を禁じるのは、実装が `ports` から import したときに、契約も shikumi-contrace も道連れにしないためである（IND_005）。`contract/ports/` を import すると、`contract/__init__.py` が先に実行される。そのため、契約資産の `__init__.py` は、空にするか、契約を import しないものにする。

## IND_014

境界の型について、次のことが望ましい。標準ライブラリにだけ依存させる（IND_004）。実装が境界の型から import するかどうかは、実装の自由であり、shikumi-contrace は求めも禁じもしない（IND_005、IND_009）。import するなら、契約を持ち出すときに、`ports` も一緒に持ち出す。

title: Guidance: depend only on the standard library, and carry ports along

level: INFORMATIVE

detail: 返したものを別のメソッドが受け取るだけの不透明なハンドルは、共有せずに、総称型の対象型で表せる（SYN_027）。既存の実装に契約を被せる場合は、実装を変えられないので、契約の側の引数型を広く設計する。標準ライブラリにだけ依存させることを検査しないのは、IND_009 による。

## IND_015

`ports` を直下に持つパッケージは、すなわち契約資産のパッケージは、テストも実装も含んではならない。

title: The package that holds ports contains no test and no implementation

level: MUST NOT

detail: 契約資産は、テストおよび実装とは別に置く（IND_001）。この規定は、その原則を、`ports` を直下に持つパッケージに適用する。実装も同居するプロジェクト全体のパッケージの直下に、`ports` を置くことはできない。契約が複数のサブパッケージに分かれていても、`ports` が契約資産のパッケージの直下にあれば、よい。範囲を宣言したときも、導出したときも、同じ規則を適用する。導出は、テストが宣言した範囲だけを使うので、束縛されていない実装は見落とす（誤検出はない）。
