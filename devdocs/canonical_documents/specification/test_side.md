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

# テスト側の記述

テストが、契約のどの条項に対して何をするのかを、テストの直前に宣言する記述を定める。条項の文は契約の側に一度だけ書き、テストはそれを参照する。

## TST_001

テストは、テストランナーが収集する通常の関数またはメソッドでなければならない。shikumi-contrace はテストの形を変えない。

title: Tests remain ordinary tests of the test runner

level: MUST

related: [AIM_003](aim.md#aim_003)

## TST_002

テストは、契約の条項に対する関係づけを、テストの直前に宣言できなければならない。関係づけは、対象の条項を、契約の実体そのものへの参照として指さなければならない。文字列で指してはならない。

title: A test declares its relation to clauses, by reference

level: MUST

related: [CTR_004](contract.md#ctr_004)

## TST_003

一つのテストは、複数の条項に関係づけられてよい。

title: One test may relate to several clauses

level: MAY

detail: 契約に基づくテストでは、一回の実行が、一つの事前条件の違反の拒否と、一つの不変条件の保持を同時に確かめることがある。

## TST_004

関係づけは、条項に対するテストの姿勢を表す関係語を伴わなければならない。標準の関係語は、`upholds`（守る）と `violates`（破る）である。

title: A relation carries a relation word

level: MUST

detail: 標準の関係語の意味は、標準語彙の仕様書に定める。

## TST_005

テストには、注釈を付けてよい。

title: Notes may be attached to a test

level: MAY

detail: 条項やテスト名からは読み取れない、判断の理由、境界の意図、注意事項を、後からテストを読む人と LLM に伝えるために用いる。

## TST_006

条項文は、契約の側に一度だけ書き、テストの側で繰り返さないことが望ましい。テスト名は、そのテストが確かめる具体的な振る舞いを表すことが望ましい。

title: Clause statements are not repeated on the test side

level: SHOULD

detail: テスト名と条項名が重なると、同じ文を二か所で保守することになる。条項文は契約に、具体的な振る舞いはテスト名に、それぞれ分けて置く。

related: [CTR_011](contract.md#ctr_011)

## TST_007

契約の対象型と実装を結び付ける束縛は、テストの側に記述しなければならない。

title: Bindings are written on the test side

level: MUST

related: [IND_007](independence.md#ind_007)

detail: 束縛の書式は、記述器と書式の仕様に定める。

## TST_008

テストの本体の内側の構造は、この仕様の範囲外であり、shikumi-contrace は規定しない。

title: The inside of a test body is out of scope

level: INFORMATIVE

related: [AIM_008](aim.md#aim_008)
