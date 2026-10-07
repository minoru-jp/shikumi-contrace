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

# 語彙

条項種別、関係づけの語、注釈の語などの語彙について、shikumi-contrace が用意するものと、利用者に委ねるものを定める。語彙は自由であるほどよい。表記ゆれは表現力の一部として受け入れる。

## VOC_001

shikumi-contrace は標準語彙を提供しなければならない。標準語彙は、条項種別、違反時の扱い、関係語、注釈語を含む。

title: A standard vocabulary is provided

level: MUST

detail: 標準の語とその意味は、標準語彙の仕様書に定める。

related: [AIM_006](aim.md#aim_006)

## VOC_002

shikumi-contrace は、利用者が独自語彙を定義して使うことを妨げてはならない。

title: Custom vocabulary is not obstructed

level: MUST NOT

related: [AIM_006](aim.md#aim_006)

## VOC_003

独自語彙は、標準語彙と同じ位置で、同じ記述方法で使えなければならない。

title: Custom vocabulary is used the same way as the standard one

level: MUST

## VOC_004

shikumi-contrace は、語彙が標準語彙に含まれないことを理由に、診断情報を出してはならない。未知の語彙を拒否してはならない。

title: Unknown vocabulary is not rejected

level: MUST NOT

detail: ここでいう拒否には、エラーだけでなく、警告も含む。語彙の取り扱いに関する診断は、利用者が自らの規定として追加した検証規則だけが出す。

## VOC_005

shikumi-contrace は、語彙の表記ゆれを統一したり、拒否したりしてはならない。

title: Variations in spelling are accepted

level: MUST NOT

detail: 表記ゆれは、あって当たり前のものである。同じ意味を別の語で書けることは、表現力を上げる。

## VOC_006

利用者は、自らの規定として語彙を制限する検証規則を、shikumi-contrace の外で定義してよい。shikumi-contrace の既定では、語彙を制限しない。

title: Restricting vocabulary is the user's choice

level: MAY

## VOC_007

注釈の語彙にも、VOC_002 から VOC_005 までの規則を同様に適用する。

title: Note vocabulary follows the same rules

level: MUST

## VOC_008

語彙は、shikumi-contrace が定義する開いた情報型（条項種別、違反時の扱い、関係、注釈）の値として表さなければならない。標準語彙も独自語彙も、同じ生成器で作る値でなければならず、独自語彙を使うために、情報型を登録する必要があってはならない。

title: Vocabulary is represented as values of open information types

level: MUST

detail: 語を情報型として登録させると、登録のない語が意味像に現れず、語彙の自由が実質的に失われる。語を値にすれば、語彙の数にかかわらず、認識する情報型は少数に保てる。

## VOC_009

独自語彙は、意味像において、標準語彙と並んで現れなければならない。

title: Custom vocabulary appears in the semantic view like the standard one

level: MUST

## VOC_010

違反時の扱いを、意図して決めずに残したいときは、プロジェクトが独自語彙の違反時の扱い（例: `UNDECIDED = define.violation("undecided")`）を定義して使ってよい。違反時の扱いの省略は、宣言していないことを表し、意図した保留とは区別できる。

title: Guidance: marking violation behavior as deliberately undecided

level: INFORMATIVE

detail: 違反時の扱いは、四つの状態を区別して読める。`REJECTED` は、違反した呼び出しを正常な成功として受理しないことまで約束する。`OUT_OF_SCOPE` は、違反時の振る舞いを約束に含めない。プロジェクトの語（`UNDECIDED` など）は、意図して未決定であることを表す。省略は、宣言していないこと（書き忘れの可能性）を表す。読み取りでは、`on_violation` が省略された事前条件は `clauses_of` を絞り込んで一覧できる。省略を許さないプロジェクトは、自らの規定として、この絞り込みを自分のテストで検査できる（VOC_006）。shikumi-contrace は、省略を診断しない。省略は正当な書き方であり、診断にすると宣言が事実上の義務になる（REG_022）。多くのプロジェクトが同じ語を必要とするようになれば、標準の語への追加を検討する。
