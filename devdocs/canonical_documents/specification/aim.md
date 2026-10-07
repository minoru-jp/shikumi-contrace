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

# 目的と範囲

shikumi-contrace が何のために存在し、何を目的としないかを定める。他の仕様書は、この文書の目的に照らして読む。

## AIM_001

shikumi-contrace の目的は、機能の約束を契約として、実装とテストから独立した資産として記述し、テストを契約の条項に結び付けて、どの条項にどのテストがあり、どのテストがどの条項に関わるのかを追えるようにすることである。契約は実装の設計に影響を与えず、設計や実装をスクラッチで作り直しても、持ち運べる。

title: Purpose: contracts as independent assets, traced by tests

level: INFORMATIVE

detail: 契約の中身（事前条件・事後条件・不変条件）は、型では検査できない。その確認はテストに委ねられるため、条項とテストの対応を追えることが重要になる。

## AIM_003

shikumi-contrace の本体は、特定のテストランナーに依存してはならない。pytest 固有の機能は、任意の連携（optional integration）として、必要最小限に提供する。

title: Independent of any test runner; pytest support is optional

level: MUST

detail: pytest 連携は shikumi-contrace の中心に置かない。導入しなくても、契約の記述、テストの関係づけ、検証は使える。

## AIM_004

shikumi-contrace は、人間と LLM の双方を、記述の書き手および読み手として想定しなければならない。

title: Humans and LLMs as both writers and readers

level: MUST

detail: 書き手として想定するとは、LLM が誤りなく書ける記述であることを求めることである。読み手として想定するとは、LLM が誤読なく読める記述であることを求めることである。人間にとっての書きやすさだけを根拠に、独自の記法を導入しない。

## AIM_005

shikumi-contrace は、事前条件・事後条件・不変条件に基づく契約を、記述できなければならない。

title: Expressing contracts of pre-conditions, post-conditions and invariants

level: MUST

detail: ここでいう契約は、事前条件・事後条件・不変条件で振る舞いを定める Design by Contract の意味である。サービス間の API 契約を検証する意味ではない。

## AIM_006

shikumi-contrace は、標準語彙を用意しつつ、独自語彙を妨げてはならない。語彙は自由であるほどよいことを、設計の原則とする。

title: Open vocabulary as a design principle

level: MUST

## AIM_007

shikumi-contrace は、Shikumi の規定体として構成しなければならない。

title: Built as a Shikumi specification body

level: MUST

detail: Shikumi が、契約情報の記述と検証に適していることは、試作で確かめた（Python 3.11 と 3.12）。基盤とする Shikumi の版は、現在の版（0.2.4）以上とし、上限は設けない。

## AIM_008

テストの本体の内側（準備、対象の呼び出し、検証の区切り）の構造化は、shikumi-contrace 自身の責務ではない。そのためのライブラリ metamk を、shikumi-contrace から再エクスポートする。

title: Structuring the inside of a test body belongs to metamk, which is re-exported

level: INFORMATIVE

detail: フェーズの意味と仕様は、metamk に属する。shikumi-contrace は、契約の側と、テストと契約の関係づけを扱う。

## AIM_009

テストロジックを再利用するための仕組みは、shikumi-contrace の目的としない。

title: Non-goal: reusing test logic

level: INFORMATIVE

detail: テストロジックの再利用は、pytest の parametrize や fixture など、テストランナーの標準の仕組みで行える。shikumi-contrace は、それらを置き換えるものを提供しない。

## AIM_010

パラメータ、スキップ、期待する例外などを、契約やテストの宣言に集約する仕組み、およびパラメータの宣言のための独自の記法は、shikumi-contrace の目的としない。

title: Non-goal: aggregating test-runner features into declarations

level: INFORMATIVE

detail: これらは、テストランナーの標準の仕組みで行える（PYT_004）。

## AIM_011

契約やテストの自動生成、および契約からテストを機械的に導出することは、shikumi-contrace の目的としない。

title: Non-goal: generating or deriving tests mechanically

level: INFORMATIVE

## AIM_012

テストの結果を契約の構造に重ねて表示すること（契約ビュー）は、shikumi-contrace の範囲外である。

title: Non-goal: a contract view of test results

level: INFORMATIVE

detail: 契約の構造を一覧にして、条項ごとにテストの結果を表示する機能は提供しない。並列実行（pytest-xdist）では、収集が worker 側で行われるため、結果の表示を契約の構造へ重ねるには追加の設計も要る。

## AIM_013

テストの構成として Arrange / Act / Assert が推奨される場合があるが、それは構成の一例にすぎない。shikumi-contrace の設計原則でも制約でもなく、shikumi-contrace はテスト本体の構成を規定しない。

title: Arrange / Act / Assert is one recommended structure, not a constraint

level: INFORMATIVE

## AIM_014

shikumi-contrace は、metamk に依存し、metamk の `Mk` を `Phase` という名前で、`phase_of` を同名で再エクスポートしなければならない。`Phase` は metamk の `Mk` と同じオブジェクトであり、`phase_of` は metamk の `phase_of` と同じオブジェクトでなければならない。

title: shikumi-contrace depends on metamk and re-exports its phase API

level: MUST

detail: metamk の版は、現在の版（0.1.0）以上とし、上限は設けない。`Phase` は、テスト本文での役割が読み取れる名前を shikumi-contrace 側で与える alias である。metamk は、依存を持たず、pytest にも依存しないため、本体が特定のテストランナーに依存しないこと（AIM_003）を損なわない。

## AIM_015

shikumi-contrace は、`Phase` と `phase_of` の意味を変更してはならない。フェーズの仕様と保守は metamk に属する。

title: The meaning of the re-exported phase API is not changed by shikumi-contrace

level: MUST NOT

detail: `Phase` は名前だけを shikumi-contrace の文脈に合わせる。振る舞いは `metamk.Mk` と同一である。

## AIM_016

shikumi-contrace は、契約に記述された意味から、テスト本体の書き方を推論してはならない。特定の例外検査、ガード節、テストランナー固有の構文などを、契約情報を理由に要求してはならない。

title: Non-goal: inferring the shape of test code from contract meaning

level: MUST NOT

detail: 契約は、人間と LLM が設計意図を読むための意味情報を保持する。例えば `REJECTED` は、違反が例外で表現されることを意味しない。例外、失敗を表す戻り値、HTTP 応答など、実装方法は契約の別の記述がない限り固定しない。
