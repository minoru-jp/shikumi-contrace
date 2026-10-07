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

# 記述器と書式

契約の側とテストの側で使う記述器の名前と書式を定める。`@=` はクラスの本体の中で、デコレータは対象の直前で用いる。語は、素の名前として import して用いる。

## SYN_001

`@=` 形式の記述は、クラスの本体の中に書く。デコレータ形式の記述は、関数、メソッド、クラスの直前に書く。

title: The @= form goes in class bodies; the decorator form goes before the target

level: MUST

detail: テストの関数とメソッドには本体がないため、テストの側の記述は、デコレータ形式で書く。

## SYN_002

対象型の指定は、記述器 `subject` を用い、契約のクラスの本体に `subject @= <subject>` と書く。

title: Writing the subject type: subject

level: MUST

related: [CTR_002](contract.md#ctr_002)

## SYN_003

メンバーが対象型のどの要素を表すかの指定は、記述器 `member` を用い、メンバーのクラスの本体に `member @= <member>` と書く。対象型が呼び出し可能な型のときは、契約の本体に書いてもよい（CTR_012）。

title: Writing the member: member

level: MUST

related: [CTR_007](contract.md#ctr_007)

## SYN_004

条項種別の指定は、記述器 `kind` を用い、条項のクラスの本体に `kind @= <kind>` と書く。

title: Writing the clause kind: kind

level: MUST

related: [CTR_004](contract.md#ctr_004)

## SYN_005

標準の条項種別の値（`PRE`、`POST`、`INV`）は大文字の識別子とし、記述器、関係語、注釈語は小文字の識別子とする。

title: Values are upper-case; descriptors and words are lower-case

level: MUST

detail: 値と、値を書くための記述器を、名前の形で見分けられるようにする。

## SYN_006

注釈語は、一つの語が、クラスの本体の `@=` 形式（`rationale @= "text"`）と、デコレータ形式（`@rationale("text")`、文を伴わない `@critical`）の、両方で使えなければならない。どの形式で書いても、付く情報は同じである。

title: An annotation word can be written in both forms

level: MUST

detail: 契約の側でも、文をデコレータ形式で書いてよい。書き方が複数あるが、結果が同じなので、書き間違いにはならない。

related: [STD_041](standard_vocabulary.md#std_041)

## SYN_007

文を伴わない注釈語（`security`、`critical` など）は、付ける対象の直前に、裸のデコレータ `@<word>` として書く。クラスの本体の中で、文を伴わないタグだけを書く形式は、提供しない。

title: A tag without text is a bare decorator

level: MUST

detail: 契約の側とテストの側で、タグの書き方を揃える。クラスの本体の `@=` 形式は、文を伴う注釈に用いる。

related: [STD_040](standard_vocabulary.md#std_040)

## SYN_008

関係語は、デコレータ形式で、テストの関数またはメソッドの直前に書く。`@upholds(<clause>, ...)` のように、一つの宣言に、複数の条項を指定できる。

title: Writing relation words: decorators taking clauses

level: MUST

related: [TST_002](test_side.md#tst_002)

## SYN_009

関係語に渡す条項は、契約のクラスそのものへの参照でなければならない。文字列など、クラスでないものが渡された場合は、デコレータを適用する時点で `TypeError` とする。渡されたクラスが条項であるかどうかは、デコレータの適用時には検査しない。

title: A relation word takes clause classes, not strings

level: MUST

related: [TST_002](test_side.md#tst_002)

## SYN_010

関係語は、テストの関数またはメソッドに付ける。テストのクラスに付けたときは、デコレータを適用する時点で `TypeError` とする。

title: Relation words are for test functions and methods

level: MUST

detail: クラスに付けたときの意味（クラスの中のすべてのテストへの適用など）は、当面定めない。黙って何も起こらない状態を避けるため、エラーにする。必要性が確認された時点で、意味を定める。

## SYN_011

`@=` 形式の記述器と語は、素の名前として import して用いなければならない。属性アクセスを経由した `@=`（例えば `c.note @= "text"`）は、モジュールが持つ記述器そのものを上書きするため、用いてはならない。

title: Use bare names for the @= form

level: MUST

detail: デコレータ形式は、名前空間を経由して書いてよい（`@c.note("text")`）。語の名前が利用者の変数名と衝突するときは、別名で import する。

## SYN_012

shikumi-contrace は、利用者が独自語彙の関係語、注釈語、条項種別、違反時の扱いを作る生成器（`define.relation(name)`、`define.annotation(name)`、`define.kind(name)`、`define.violation(name)`）を提供しなければならない。標準語彙も、同じ生成器で作る。

title: Generators create custom and standard words alike

level: MUST

detail: 生成した語は、`flaky = define.annotation("flaky")` のように、同じ名前の変数に束縛して用いる。変数名と文字列が重なるが、語の名前は変数名に依存しない。生成器の名前は、利用者の変数名と衝突しにくいように、`words` ではなく `define` とする。

## SYN_013

記述器と語には、型チェッカーが、文を伴う形式（`@note("text")`）と、伴わない形式（`@security`）、および `@=` 形式を、区別して検査できる型注釈を付けなければならない。

title: Type annotations distinguish the forms

level: MUST

detail: デコレータの対象を表す型変数は、関数、メソッド、クラスに制約する。制約がないと、文を伴う形式が、対象を受け取る形式と取り違えられる。

## SYN_014

デコレータ形式で付けた情報の保持の順は、適用された順（書いた順の逆）である。`@=` 形式で付けた情報の保持の順は、書いた順である。

title: Order in which information is held

level: INFORMATIVE

detail: 読み取り API は、この違いを吸収して、書いた順で返す（RDG_009）。

## SYN_015

束縛は、デコレータ `@binds[<subject>](<implementation>, ...)` として、テストのクラス、または関数・メソッドの直前に書く。

title: Writing the binding: binds

level: MUST

related: [IND_007](independence.md#ind_007)

## SYN_016

`binds` には、型引数で対象型を指定しなければならない。型引数を省いた場合は、デコレータを適用する時点で `TypeError` とする。

title: binds takes the subject type as a type argument

level: MUST

detail: 型引数を省くと、型チェッカーが実装の適合を検査できない。検査しているように見えて、実際には検査されない書き方は、提供しない。

## SYN_017

`binds` には、実装を一つ以上渡せる。実装は、対象型を作るもの（クラス、またはそれを返す関数）か、対象型そのもの（関数、module、オブジェクト）である。構築に必要な引数の有無は問わない。

title: binds takes implementations: factories or objects

level: MUST

detail: 関数一つを対象とする契約には関数そのものを、関数の集まりを対象とする契約には module そのものを渡す。実装が作るものか、そのものかは、実行時には区別しない。

related: [CTR_012](contract.md#ctr_012)

## SYN_018

束縛は、付けた対象に適用する。テストのクラスに付けたときは、そのクラスの中のテストに適用する。クラスと、その中の関数・メソッドの両方に束縛が付いたときは、両方を適用する。モジュール全体への束縛は、当面提供しない。

title: A binding applies to the decorated target

level: MUST

detail: 関係語（SYN_010）と異なり、束縛はテストのクラスに付けられる。束縛は、どの実装に対するテストかを表す宣言であり、クラス単位が自然であるため。

## SYN_019

`binds` の型注釈は、実装が対象型に適合しないときに、型チェッカーが検出できるものでなければならない。

title: A non-conforming implementation is detected by the type checker

level: MUST

detail: 契約を持ち出して実装を作り直したとき、新しい実装が対象型に適合しているかを、実行前に知れる。適合の検査は、basedpyright と mypy で確認した。関数、module、ジェネリックな関数、オーバーロードされた関数を実装とする場合も同様である。

## SYN_020

束縛は宣言であり、強制ではない。shikumi-contrace は、テストが束縛された実装を実際に使っているかを、検証しない。

title: A binding is a declaration, not an enforcement

level: INFORMATIVE

## SYN_021

`@=` 形式の記述器は、値の検査を、`@=` を評価する時点で行わなければならない。クラスの生成時に行う処理の中で、例外を出してはならない。

title: Values of @= descriptors are checked when @= is evaluated

level: MUST

detail: Python 3.11 では、クラスの生成時に行う処理の中で出た例外が、`RuntimeError` に包まれ、原因が分かりにくくなる。Python 3.12 以降では、元の例外がそのまま出る。

## SYN_022

利用者は、metamk の `Mk` を `Phase` という名前で、`phase_of` を同名で、`shikumi_contrace` から import して使える。

title: metamk phase names can be imported from shikumi_contrace

level: MUST

detail: 例えば、`from shikumi_contrace import Phase` と書ける。`Phase` は `from metamk import Mk` で得るものと同じオブジェクトを指す。

## SYN_023

再エクスポートは、明示的な alias または `__all__` で公開名を示すことが望ましい。

title: Re-exports are written in the explicit form

level: SHOULD

detail: 例えば `from metamk import Mk as Phase` と書く。型チェッカーによっては、明示のない再エクスポートを公開名として扱わない（mypy の `--no-implicit-reexport` など）。

## SYN_024

`@=` 形式の記述器は、`@=` の結果の型を、記述器自身の型として注釈しなければならない。

title: The result of @= is annotated as the descriptor itself

level: MUST

detail: クラス本体の `name @= value` は、名前 `name` への代入であり、mypy は、結果の型が `name` の型と違うと、すべての行に誤りを出す。結果を記述器自身の型（`Self`）と注釈すれば、basedpyright と mypy の両方が受け入れる。実行時には、Shikumi が、クラスの生成時に取り除く、一時的な束縛が返る。

## SYN_025

契約依存は、記述器 `depends_on` を用い、依存元の契約のクラス本体に `depends_on @= <contract>` と書く。依存先は、別の契約のクラスそのものへの参照でなければならず、文字列であってはならない。複数の依存先は、`depends_on @= ...` を複数回、書いた順に記述する。

title: Writing contract dependencies: depends_on

level: MUST

related: [CTR_014](contract.md#ctr_014)

detail: クラスそのものへの参照だけを受け取るため、通常の記述では、まだ定義されていない契約への forward reference は作らない。循環は検証でも診断する。

## SYN_026

違反時の扱いは、記述器 `on_violation` を用い、事前条件の条項のクラス本体に `on_violation @= <behavior>` と書く。標準値は `OUT_OF_SCOPE` と `REJECTED` である。独自の違反時の扱いは `define.violation(<name>)` で作る。

title: Writing precondition violation behavior: on_violation

level: MUST

related: [CTR_016](contract.md#ctr_016)

detail: `on_violation` は、違反時の実装手段を指定しない。`REJECTED` であっても、例外を投げることや `pytest.raises` を使うことを意味しない。

## SYN_027

`binds` の型引数には、対象型のクラスそのものに加えて、総称型のクラスに型引数を与えたもの（`Subject[Handle]`）を渡せる。束縛が記録するのは、型引数を与える前のクラス（`Subject`）である。契約の側は、型引数を与えないクラスを `subject @= Subject` と書く。

title: binds accepts a generic subject given type arguments

level: MUST

related: [IND_006](independence.md#ind_006)

detail: 実装が自分の型の値を返し、別のメソッドがその値を受け取る場合（予約を返す `reserve` と、予約を受け取る `release` など）、契約は、その型を型変数にした総称の Protocol で、「返したものを受け取る」という関係を、実装の型を契約へ持ち込まずに書ける。束縛で `@binds[Inventory[Reservation]](Impl)` と書くと、型チェッカーは、型引数を含めて適合を検査する（basedpyright と mypy で確認した）。型引数は型検査のためだけにあり、束縛には記録しない。読み取りは、型引数を与える前のクラスを返す。型引数を与えない総称型のクラスも、実行時には受理する。型チェッカーの設定によっては、型引数がないことを警告する。型引数は、クラスに対してだけ与えられる。ユニオン（`A | B`）や `Annotated` などは、対象型として受理せず、`TypeError` とする（SYN_016）。
