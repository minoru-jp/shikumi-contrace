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

# 公開 API の名前と配置

公開 API を置く場所と、読み取り API、検証 API、pytest 連携の名前を定める。契約とテストを書くための名前（記述器、語、束縛）は、記述器と書式の仕様に定める。

## API_001

本体の公開 API は、`shikumi_contrace`（最上位）、`shikumi_contrace.reading`、`shikumi_contrace.checking` に置き、pytest連携は `shikumi_contrace.pytest` に置く。

title: Public APIs are placed in four locations

level: MUST

## API_002

最上位の `shikumi_contrace` には、契約とテストを書くための名前を、平らに置く。記述器（`subject`、`member`、`kind`、`depends_on`、`on_violation`）、条項種別の値（`PRE`、`POST`、`INV`）、標準の違反時の扱い（`OUT_OF_SCOPE`、`REJECTED`）、関係語、注釈語、`binds`、独自語彙の生成器 `define`、metamk の再エクスポート（`Phase`、`phase_of`。`Phase` は `metamk.Mk` の alias）である。

title: The top level holds the names for writing contracts and tests

level: MUST

detail: `@=` 形式の記述器は、素の名前として import して使う（SYN_011）ため、書くための名前は、最上位に平らに置く。

related: [SYN_011](syntax.md#syn_011)

## API_003

読み取り API は `shikumi_contrace.reading` に、検証 API は `shikumi_contrace.checking` に置き、最上位には置かない。

title: Reading and checking APIs are not placed at the top level

level: MUST

detail: 契約とテストを書くコードに必要なのは、書くための名前だけである。読む名前や検査する名前を最上位に混ぜると、利用者の名前との衝突のおそれと、名前の数が増える。契約資産が、必要最小限の名前だけを import することにも合う（IND_004）。

related: [RDG_001](reading.md#rdg_001)

## API_004

`shikumi_contrace.reading` は、次の関数を提供する。名前は、Shikumi の `information_of` と同じ「`*_of`」の形に揃える。

| 名前 | 役割 |
| --- | --- |
| `relations_of(test)` | テストの関係づけ（関係語と条項） |
| `annotations_of(obj)` | 注釈（語と文） |
| `bindings_of(obj)` | 束縛（対象型と実装） |
| `clauses_of(contract)` | 契約の条項の一覧（種別、違反時の扱い、条項文、注釈） |
| `dependencies_of(contract)` | 契約が直接依存する契約を、書いた順に読む |
| `dependents_of(contract, within=...)` | 契約に直接依存する契約を、指定した範囲で逆引きする |
| `tests_of(clause, within=...)` | 条項から、関係づけしたテストを逆引きする |
| `untested_clauses(contract, within=...)` | 関係づけを持つテストのない条項の一覧 |

title: Names of the reading API

level: MUST

detail: `within` には、逆引きや一覧の範囲とする対象を渡す。`tests_of` と `untested_clauses` にはテストを、`dependents_of` には契約を含む module または class を渡す（RDG_004、RDG_010）。`untested_clauses` は、条項の意味からテストの要否を推論せず、記録された関係づけの有無だけを見る（RDG_005）。

related: [RDG_002](reading.md#rdg_002), [RDG_010](reading.md#rdg_010)

## API_005

`shikumi_contrace.reading` は、読み取り結果の型として、`Relation`、`Annotation`、`Binding`、`Clause` を提供する。`__wrapped__` をたどる読み取り（RDG_007）は、API_004 の関数がすべて内蔵する。

title: Result types of the reading API

level: MUST

related: [RDG_007](reading.md#rdg_007)

## API_006

`shikumi_contrace.checking` は、検証を実行して診断情報のリスト（`list[Diagnostic]`）を返す `check(...)`、診断情報の型 `Diagnostic`（コード、メッセージ、対象）、pytest連携が診断情報を報告する警告のカテゴリ `ContraceWarning`、契約資産の構造の規定 `CONTRACT_ASSET_STRUCTURE` を提供する。リストが空であれば、違反はない。

title: Names of the checking API

level: MUST

detail: `check` が返す型は、shikumi-contrace 自身の型とし、Shikumi の検証結果の型を、公開 API に出さない。`CONTRACT_ASSET_STRUCTURE` は、Shikumi の型の値であり、Shikumi 自身の検証に渡すために公開する、唯一の名前である（REG_027）。

related: [REG_018](regulation.md#reg_018)

## API_007

`check` は、範囲を、宣言（`contract_assets`、`tests`、`implementations`: モジュールパスの文字列のリスト）、または導出の元（`test_modules`: テストのモジュールのリスト）で受け取る。三つの宣言のうち、一つでも指定されたときは、導出を用いず、指定されない役割の範囲は空とする。

title: How check receives the ranges

level: MUST

detail: 範囲の宣言は、宣言があれば宣言のみを用いる（REG_011）という規則を、部分的な宣言にも適用したものである。

related: [REG_011](regulation.md#reg_011)

## API_008

pytest連携は、利用者が、`pytest_plugins = ["shikumi_contrace.pytest"]` と書いて、明示的に登録する。

title: The pytest integration is registered explicitly

level: MUST

detail: パッケージの中に、`pytest.py` という名前のモジュールがあっても、絶対 import により、本物の pytest が読み込まれ、動作することを確認した。

related: [PYT_005](pytest_integration.md#pyt_005)

## API_009

収集時の検証は、オプション `--contrace-check` で選ぶ。範囲の宣言は、pytest の設定（ini）の `contrace_contract_assets`、`contrace_tests`、`contrace_implementations` に、モジュールパスを一行ずつ書く。

title: The option and the settings of the pytest integration

level: MUST

detail: 設定の三つのキーは、`check` の三つの宣言に対応する。

related: [PYT_012](pytest_integration.md#pyt_012)

## API_010

診断情報を、警告からエラーに引き上げるには、pytest の警告のフィルタ（`-W error::shikumi_contrace.checking.ContraceWarning`、または設定の `filterwarnings`）を用いる。

title: Escalating diagnostics to errors

level: INFORMATIVE

related: [PYT_007](pytest_integration.md#pyt_007)
