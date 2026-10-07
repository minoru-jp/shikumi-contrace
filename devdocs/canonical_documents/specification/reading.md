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

# 情報の読み取り

条項とテストの対応を追えるようにするため、宣言された情報を読み取る API を定める。pytest 連携は必要最小限に留めるため、絞り込みや一覧などは、この API を用いて、利用者が書ける。API の名前は、公開 API の名前と配置の仕様に定める。

## RDG_001

本体は、宣言された契約とテストの情報を読み取る API を提供しなければならない。この API は、特定のテストランナーに依存してはならない。

title: A reading API independent of any test runner

level: MUST

related: [AIM_003](aim.md#aim_003)

## RDG_002

読み取り API は、テストが持つ関係づけ（関係語と条項）、注釈、束縛を読めなければならない。

title: Reading what a test declares

level: MUST

detail: テストのクラスに付けた束縛も、そのクラスの中のテストの束縛として読める（SYN_018）。関数のオブジェクトからクラスを辿るのは、`__qualname__` による解決で、モジュール直下のクラスに限る。インスタンスのメソッドからは、インスタンスのクラスを辿れるので、関数の中で定義したクラスも読める。関数の中で定義したクラスの、関数のオブジェクトからは辿れない。pytest 連携は、収集したクラスから直接読むので、影響しない。

## RDG_003

読み取り API は、契約が持つ条項の一覧（種別、違反時の扱い、条項文、注釈を含む）を、契約から読めなければならない。

title: Reading the clauses of a contract

level: MUST

## RDG_004

読み取り API は、条項から、その条項に関係づけしたテストを逆引きできなければならない。逆引きは、利用者が渡したテストの範囲で行う。

title: Looking up the tests related to a clause

level: MUST

related: [AIM_001](aim.md#aim_001)

## RDG_005

読み取り API は、関係づけを持つテストのない条項を、一覧できなければならない。

title: Listing clauses that no test is related to

level: MUST

detail: この一覧は、記録された関係づけの有無だけを示す。条項の種別、違反時の扱い、その他の意味から、その条項にテストが必要かどうかを推論しない。

related: [AIM_001](aim.md#aim_001)

## RDG_006

読み取り API は、情報を読むだけでなければならない。契約やテストの内容を書き換えてはならない。

title: The reading API only reads

level: MUST NOT

## RDG_007

読み取り API は、デコレータが包んだ関数について、`__wrapped__` の連鎖をたどって、内側の関数に付いた情報も読まなければならない。外側と内側の両方に付いた情報は、両方を返す。

title: The reading API follows the __wrapped__ chain

level: MUST

detail: 情報は、オブジェクトの同一性に付く。宣言が、他のデコレータ（`functools.wraps` を使うものや `mock.patch` など）より内側にあると、情報は内側の関数に付き、外側のラッパー関数には付かない。連鎖をたどらないと、そのような宣言を読み落とす。

## RDG_008

テストの関数とメソッドは、Shikumi の実体として扱わない。テストの情報は、関数やメソッドのオブジェクトから、直接読む。

title: Test functions are read directly, not as Shikumi entities

level: INFORMATIVE

detail: Shikumi の標準の構造は、クラスを実体として扱い、関数とメソッドを実体として扱わない。契約の側（クラス）の検証には、Shikumi の検証の枠組みを用いるが、テストの側の情報は、読み取り API で読む。テストの側に関わる検証規則（REG_010 など）も、読み取り API を用いて実装できる。

## RDG_009

読み取り API は、情報を、書いた順に返さなければならない。同じ対象にデコレータで付けた情報は、上から下の順に、クラスの本体の `@=` で付けた情報は、デコレータで付けた情報の後に、書いた順に返す。外側のラッパーの情報は、内側の関数の情報より先に返す。

title: Information is returned in the order it was written

level: MUST

detail: デコレータは、下から適用されるため、付けた情報の保持の順は、書いた順の逆になる（SYN_014）。読み取り API が、これを吸収する。

## RDG_010

読み取り API は、契約から、その契約が直接依存する契約を、書いた順で読めなければならない。また、利用者が渡した範囲の中で、ある契約に直接依存する契約を逆引きできなければならない。逆方向の関係は保存せず、宣言された一方向の契約依存から求める。

title: Reading contract dependencies in both directions

level: MUST

related: [AIM_003](aim.md#aim_003)
