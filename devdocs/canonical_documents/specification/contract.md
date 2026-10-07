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

# 契約の構造

契約を、対象型、メンバー、条項というクラスの入れ子として記述するときの構造を定める。Shikumi が扱う粒度はクラスまでであるため、メソッド単位の条項もクラスで表す。

## CTR_001

契約は、対象型の指定と条項を含む、Python のクラスとして記述されなければならない。

title: A contract is a class

level: MUST

related: [AIM_001](aim.md#aim_001)

## CTR_002

一つの契約は、一つの対象型を、その型そのものへの参照として指定しなければならない。文字列による指定であってはならない。

title: A contract names one subject type by reference

level: MUST

detail: 対象型を文字列で指すと、契約が必要以上に汎化され、IDE から辿ることもできなくなる。契約は型を保ったまま記述する。

## CTR_003

契約が定義する型は、構造的な型（Protocol）でなければならない。dataclass などの具象クラスを契約に置いてはならない。

title: Types defined by a contract are structural

level: MUST

detail: 実装が契約を import せず、自前の型を持ったまま、構造的に適合できるようにするため。値を表す型も、必要な属性を読み取り専用のプロパティとして持つ構造的な型で表す。

related: [AIM_001](aim.md#aim_001)

## CTR_004

条項は、契約またはメンバーの中に入れ子にしたクラスとして記述し、クラスの docstring を条項文としなければならない。一つの条項は、一つの約束を一文で述べる。

title: A clause is a nested class whose docstring is the clause statement

level: MUST

## CTR_005

対象型全体に対する条項は、契約の直下に置かなければならない。

title: Clauses about the whole subject type sit directly under the contract

level: MUST

## CTR_006

メンバーは、対象型のメソッドなどを表す、契約の直下の入れ子クラスとして記述し、そのメンバーに対する条項は、メンバーのクラスの中に置かなければならない。対象型が呼び出し可能な型である場合は、CTR_012 に従ってもよい。

title: A member is a nested class that holds the clauses of one method

level: MUST

detail: Shikumi は、クラスより細かい粒度であるメソッドを実体として扱わない。そのため、メソッド単位の条項も、メソッドを表すクラスを介して表す。

## CTR_007

メンバーは、対象型のどのメンバーを表すかを、対象型のそのメンバーへの参照として指定しなければならない。

title: A member refers to the member of the subject type

level: MUST

## CTR_008

メンバーのクラス名は、参照先の対象型のメンバー名と一致していることが望ましい。一致しない場合は診断する。ただし、対象型の指定とメンバーの指定を同時に持つ契約（CTR_012）は、この規則の対象としない。

title: Member class names follow the referred member names

level: SHOULD

detail: IDE のリネームで、参照先の名前だけが変わったときのずれを検出するための保険になる。

## CTR_009

標準語彙の事前条件と事後条件は、メンバーを表す実体（メンバーのクラス、または CTR_012 により `member` を持つ契約）の直下に置かなければならない。標準語彙の不変条件は、対象型の指定を持つ契約の直下に置かなければならない。置く位置が異なる場合は診断する。独自語彙の条項種別は、この位置の規則の対象としない。

title: Standard clause kinds have fixed positions

level: MUST

detail: 位置には役割を与え、そこに入れる言葉は縛らない。位置の規則は標準語彙にだけ適用し、独自語彙は妨げない。契約が対象型の指定とメンバーの指定の両方を持つ場合は、事前条件、事後条件、不変条件のいずれも、契約の直下に置ける。

## CTR_010

注釈は、契約、メンバー、条項のいずれにも付けてよい。

title: Notes may be attached to a contract, a member, or a clause

level: MAY

## CTR_011

条項文は、その条項だけを読んで意味が分かるように書くことが望ましい。他の条項やテストを読まなければ意味が分からない書き方は避ける。

title: A clause statement is readable on its own

level: SHOULD

## CTR_012

対象型が呼び出し可能な型、すなわち `__call__` だけを持つ Protocol であるとき、契約のクラス自身が、その `__call__` を表してよい。そのためには、契約の本体に、対象型の指定に加えて、`member @= <subject>.__call__` を書く。このとき、メンバーのクラスは要らず、事前条件と事後条件の条項を、契約の直下に置ける。

title: A contract may itself stand for the single member of a callable subject type

level: MAY

detail: 関数一つを対象とする契約は、`__call__` だけを持つ Protocol（callback protocol）を対象型にして書く。新しい記述器は要らない。

## CTR_013

関数の集まり（module）を対象とする契約は、メソッドを持つ通常の対象型で書き、module は実装として束縛する。

title: A contract for a module of functions uses an ordinary subject type

level: INFORMATIVE

detail: module を束縛する書式は、記述器と書式の仕様に定める。

## CTR_014

契約は、一つ以上の別の契約への契約依存を持ってよい。`B` が `A` に依存するとは、`A` の変更または廃止によって、`B` の妥当性または存続意義を再評価する必要が生じることを表す。

title: A contract may depend on other contracts

level: MAY

detail: 依存は論理的な含意ではなく、変更の影響を追跡するための一方向の関係である。依存先の変更や廃止によって、依存元を自動的に変更または廃止しない。複数の依存先を持ってよい。

## CTR_015

契約依存は循環してはならない。直接の相互依存だけでなく、複数の契約を経由して依存元へ戻る依存も認めない。

title: Contract dependencies are acyclic

level: MUST

## CTR_016

事前条件の条項は、違反時の扱いを持ってよい。違反時の扱いは、その事前条件を満たさない呼び出しについて、その条項自身がどこまでを約束の範囲に含めるかを表す。

title: A precondition may declare how violation is treated

level: MAY

detail: 違反時の扱いを書かないことは、`OUT_OF_SCOPE` を書いたこととは同じではない。省略は、違反時の扱いについて、この情報を宣言していないことを表す。
