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

# pytest 連携（任意）

shikumi-contrace の本体は、特定のテストランナーに依存しない。この文書は、pytest 向けの機能を任意の連携として提供するときに、shikumi-contrace が守ること、および連携が提供する機能の範囲を定める。連携は必要最小限に留め、それ以外は、本体の読み取り API で行う。

## PYT_001

テストの収集と実行は、テストランナー（pytest）が行う。shikumi-contrace は、それらを独自に実装してはならない。

title: Collection and execution belong to the test runner

level: MUST NOT

related: [AIM_003](aim.md#aim_003)

## PYT_002

shikumi-contrace は、メタクラスやクラス名の書き換えなどによって、テスト関数やテストクラスを生成したり、書き換えたりしてはならない。

title: Tests are not synthesized or rewritten

level: MUST NOT

## PYT_003

テストランナーから見えるテスト関数の名前、署名、定義位置を、shikumi-contrace が変更してはならない。

title: Names, signatures and locations of tests are preserved

level: MUST NOT

detail: テストランナーの出力、IDE、トレースバックが、実際の定義位置を指すようにするため。

## PYT_004

shikumi-contrace は、pytest の標準の機構（parametrize、fixture、mark、skip など）と共存しなければならない。それらを置き換える機構を提供してはならない。

title: Coexistence with the standard mechanisms of pytest

level: MUST

related: [AIM_009](aim.md#aim_009)

## PYT_005

pytest連携は、任意でなければならない。pytest連携を導入しなくても、契約の記述、テストの関係づけ、検証は使えなければならない。

title: The pytest integration is optional

level: MUST

related: [AIM_003](aim.md#aim_003)

detail: 導入の形態は、PYT_016 に定める。

## PYT_006

本体は、pytest を import してはならない。pytest に依存する処理は、pytest連携にだけ置かなければならない。

title: The core does not import pytest

level: MUST

related: [IND_004](independence.md#ind_004)

detail: 契約資産は、shikumi-contrace の本体を import する。本体が pytest を import すると、契約資産が pytest に依存してしまい、契約を独立した資産として持ち出しにくくなる。

## PYT_007

pytest連携が報告する診断情報は、pytest の警告として報告しなければならない。診断情報の重大度は、利用者が pytest の警告のフィルタ（`-W` や `filterwarnings`）で決められなければならない。

title: Diagnostics are reported as pytest warnings

level: MUST

detail: 診断情報を警告として出すことで、既定では実行を止めず、利用者が必要に応じてエラーへ引き上げられる。警告をエラーとして扱う指定がされた場合は、pytest の内部エラーとしてではなく、診断の内容が分かる通常のエラーとして終了する。

## PYT_008

shikumi-contrace は、契約とテストの情報を、Shikumi の情報としてオブジェクトに保持しなければならない。

title: Information is held as Shikumi information

level: MUST

## PYT_009

pytest連携は、pytest が収集したテストから、本体が付けた情報を読まなければならない。そのために、テストの関数やメソッドの定義位置、名前、署名を変更してはならない。情報の読み方は、読み取り API（RDG_007 を含む）に従う。

title: The integration reads information from collected tests

level: MUST

related: [RDG_007](reading.md#rdg_007)

## PYT_010

pytest連携が提供する機能は、契約情報の表示など、必要最小限に限ることが望ましい。提供する機能は、PYT_011 から PYT_013 に定める。

title: The integration is kept to the necessary minimum

level: SHOULD

detail: 契約ビュー（テスト結果を契約の構造に重ねて表示すること）は範囲外である。

related: [AIM_003](aim.md#aim_003)

## PYT_011

pytest連携は、失敗したテストの出力に、そのテストが関係づけした条項（種別と条項文）、注釈、束縛した実装を表示しなければならない。この表示は常に有効とし、契約の宣言を持たないテストの出力には、何も加えてはならない。

title: Contract information is shown in the output of failed tests

level: MUST

detail: テストのクラスに付けた束縛も表示する。並列実行でも表示される。表示は、関係づけ、注釈、束縛の順に、一行ずつとする。関係づけと注釈は、書いた順（RDG_009）に並べる。条項文は、最初の一行を表示する。

related: [AIM_003](aim.md#aim_003)

## PYT_012

pytest連携は、収集時に検証を実行して、診断情報を報告する機能を提供しなければならない。診断情報の報告は、PYT_007 に従う。この機能は、利用者が選んだときだけ動作しなければならない。

title: Validation at collection time runs only when the user chooses it

level: MUST

detail: 導入しただけで、既存のテストに警告が出ることを避ける。本体の API を用いて、通常のテストの中から、同じ検証を呼ぶこともできる。選ぶ手段の名前は、公開 API の名前と配置の仕様に定める。検証を選ばなければ、保証は働かないため、継続的な検証では、設定で常に選んでおくことが望ましい。

related: [AIM_003](aim.md#aim_003)

## PYT_013

並列実行（pytest-xdist）では、収集時の検証は、一つの worker だけが実行して報告しなければならない。診断情報を、worker の数だけ重複して報告してはならない。

title: Under parallel execution, validation runs in a single worker

level: MUST

detail: 各 worker は、すべてのテストを収集するので、一つの worker で検証できる。この動作は、pytest-xdist が worker に渡す情報に依存している。対象は pytest-xdist に限る。他の並列実行プラグインでの動作は、規定しない。

## PYT_014

条項種別などによるテストの絞り込みのオプションは、標準では提供しない。

title: No built-in option for filtering tests by contract information

level: INFORMATIVE

detail: pytest の `-m` は、マークの引数で絞り込めない。利用者は、本体の読み取り API を用いて、`conftest.py` に、絞り込みを書ける。

## PYT_015

pytest連携は、契約とテストの情報を、`pytest.mark` に記録する機能を提供しない。

title: Information is not recorded as pytest marks

level: INFORMATIVE

detail: 語彙が自由であるため、マークの種類が際限なく増え、`--strict-markers` とも相性が悪い。引数による絞り込みも、`-m` ではできない。必要な利用者は、pytest 標準のマークを、自分で付けられる。

## PYT_016

pytest連携は、追加の依存関係として導入できなければならない。pytest への登録は、利用者が明示しなければならない。導入しただけで、pytest の動作が変わってはならない。

title: The pytest integration is an optional extra with explicit registration

level: MUST

detail: 例えば、`pip install shikumi-contrace[pytest]` で導入し、利用者が、`conftest.py` などに登録を書く。自動で登録すると、shikumi-contrace を別の目的で入れただけの環境でも、pytest の動作が変わる。

related: [AIM_003](aim.md#aim_003)
