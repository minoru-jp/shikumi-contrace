"""記述器と書式の仕様。契約とテストの側で、どの名前を、どう書くか。"""

from shikumi_devdoc.fields.specification import (
    INFORMATIVE,
    MUST,
    SHOULD,
    detail,
    level,
    related,
)
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import title

from devdocs.canonical_sources.specification.contract import (
    SPECIFICATION_PART as CONTRACT,
)
from devdocs.canonical_sources.specification.independence import (
    SPECIFICATION_PART as INDEPENDENCE,
)
from devdocs.canonical_sources.specification.standard_vocabulary import (
    SPECIFICATION_PART as STANDARD_VOCABULARY,
)
from devdocs.canonical_sources.specification.test_side import (
    SPECIFICATION_PART as TEST_SIDE,
)
from devdocs.canonical_sources.vocabulary import TERMS


@summary("契約とテストの側で使う記述器の名前と、その書式。束縛の書式を含む。")
@canonical_source(
    "記述器と書式",
    filename="syntax.md",
    order=45,
    merge_policy="local",
    heading="identity",
)
class SPECIFICATION_PART:
    """契約の側とテストの側で使う記述器の名前と書式を定める。`@=` はクラスの本体の中で、デコレータは対象の直前で用いる。語は、素の名前として import して用いる。"""

    class SYN_001:
        """`@=` 形式の記述は、クラスの本体の中に書く。デコレータ形式の記述は、関数、メソッド、クラスの直前に書く。"""

        title @= "The @= form goes in class bodies; the decorator form goes before the target"
        level @= MUST
        detail @= "テストの関数とメソッドには本体がないため、テストの側の記述は、デコレータ形式で書く。"

    class SYN_002:
        """{{TERM_002}}の指定は、記述器 `subject` を用い、{{TERM_001}}のクラスの本体に `subject @= <subject>` と書く。"""

        title @= "Writing the subject type: subject"
        level @= MUST
        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_002
        related @= CONTRACT.CTR_002

    class SYN_003:
        """{{TERM_003}}が対象型のどの要素を表すかの指定は、記述器 `member` を用い、メンバーのクラスの本体に `member @= <member>` と書く。対象型が呼び出し可能な型のときは、契約の本体に書いてもよい（CTR_012）。"""

        title @= "Writing the member: member"
        level @= MUST
        merge @= TERMS.TERM_003
        related @= CONTRACT.CTR_007

    class SYN_004:
        """{{TERM_005}}の指定は、記述器 `kind` を用い、{{TERM_004}}のクラスの本体に `kind @= <kind>` と書く。"""

        title @= "Writing the clause kind: kind"
        level @= MUST
        merge @= TERMS.TERM_004
        merge @= TERMS.TERM_005
        related @= CONTRACT.CTR_004

    class SYN_005:
        """標準の条項種別の値（`PRE`、`POST`、`INV`）は大文字の識別子とし、記述器、{{TERM_019}}、{{TERM_020}}は小文字の識別子とする。"""

        title @= "Values are upper-case; descriptors and words are lower-case"
        level @= MUST
        merge @= TERMS.TERM_019
        merge @= TERMS.TERM_020
        detail @= "値と、値を書くための記述器を、名前の形で見分けられるようにする。"

    class SYN_006:
        """{{TERM_020}}は、一つの語が、クラスの本体の `@=` 形式（`rationale @= "text"`）と、デコレータ形式（`@rationale("text")`、文を伴わない `@critical`）の、両方で使えなければならない。どの形式で書いても、付く情報は同じである。"""

        title @= "An annotation word can be written in both forms"
        level @= MUST
        merge @= TERMS.TERM_020
        detail @= "契約の側でも、文をデコレータ形式で書いてよい。書き方が複数あるが、結果が同じなので、書き間違いにはならない。"
        related @= STANDARD_VOCABULARY.STD_041

    class SYN_007:
        """文を伴わない{{TERM_020}}（`security`、`critical` など）は、付ける対象の直前に、裸のデコレータ `@<word>` として書く。クラスの本体の中で、文を伴わないタグだけを書く形式は、提供しない。"""

        title @= "A tag without text is a bare decorator"
        level @= MUST
        merge @= TERMS.TERM_020
        detail @= "契約の側とテストの側で、タグの書き方を揃える。クラスの本体の `@=` 形式は、文を伴う注釈に用いる。"
        related @= STANDARD_VOCABULARY.STD_040

    class SYN_008:
        """{{TERM_019}}は、デコレータ形式で、テストの関数またはメソッドの直前に書く。`@upholds(<clause>, ...)` のように、一つの宣言に、複数の{{TERM_004}}を指定できる。"""

        title @= "Writing relation words: decorators taking clauses"
        level @= MUST
        merge @= TERMS.TERM_004
        merge @= TERMS.TERM_019
        related @= TEST_SIDE.TST_002

    class SYN_009:
        """{{TERM_019}}に渡す{{TERM_004}}は、契約のクラスそのものへの参照でなければならない。文字列など、クラスでないものが渡された場合は、デコレータを適用する時点で `TypeError` とする。渡されたクラスが条項であるかどうかは、デコレータの適用時には検査しない。"""

        title @= "A relation word takes clause classes, not strings"
        level @= MUST
        merge @= TERMS.TERM_004
        merge @= TERMS.TERM_019
        related @= TEST_SIDE.TST_002

    class SYN_010:
        """{{TERM_019}}は、テストの関数またはメソッドに付ける。テストのクラスに付けたときは、デコレータを適用する時点で `TypeError` とする。"""

        title @= "Relation words are for test functions and methods"
        level @= MUST
        merge @= TERMS.TERM_019
        detail @= "クラスに付けたときの意味（クラスの中のすべてのテストへの適用など）は、当面定めない。黙って何も起こらない状態を避けるため、エラーにする。必要性が確認された時点で、意味を定める。"

    class SYN_011:
        """`@=` 形式の記述器と語は、素の名前として import して用いなければならない。属性アクセスを経由した `@=`（例えば `c.note @= "text"`）は、モジュールが持つ記述器そのものを上書きするため、用いてはならない。"""

        title @= "Use bare names for the @= form"
        level @= MUST
        detail @= 'デコレータ形式は、名前空間を経由して書いてよい（`@c.note("text")`）。語の名前が利用者の変数名と衝突するときは、別名で import する。'

    class SYN_012:
        """shikumi-contrace は、利用者が{{TERM_012}}の{{TERM_019}}、{{TERM_020}}、{{TERM_005}}、{{TERM_023}}を作る{{TERM_021}}（`define.relation(name)`、`define.annotation(name)`、`define.kind(name)`、`define.violation(name)`）を提供しなければならない。{{TERM_011}}も、同じ{{TERM_021}}で作る。"""

        title @= "Generators create custom and standard words alike"
        level @= MUST
        merge @= TERMS.TERM_005
        merge @= TERMS.TERM_011
        merge @= TERMS.TERM_012
        merge @= TERMS.TERM_023
        merge @= TERMS.TERM_019
        merge @= TERMS.TERM_020
        merge @= TERMS.TERM_021
        detail @= '生成した語は、`flaky = define.annotation("flaky")` のように、同じ名前の変数に束縛して用いる。変数名と文字列が重なるが、語の名前は変数名に依存しない。生成器の名前は、利用者の変数名と衝突しにくいように、`words` ではなく `define` とする。'

    class SYN_013:
        """記述器と語には、型チェッカーが、文を伴う形式（`@note(\"text\")`）と、伴わない形式（`@security`）、および `@=` 形式を、区別して検査できる型注釈を付けなければならない。"""

        title @= "Type annotations distinguish the forms"
        level @= MUST
        detail @= "デコレータの対象を表す型変数は、関数、メソッド、クラスに制約する。制約がないと、文を伴う形式が、対象を受け取る形式と取り違えられる。"

    class SYN_014:
        """デコレータ形式で付けた情報の保持の順は、適用された順（書いた順の逆）である。`@=` 形式で付けた情報の保持の順は、書いた順である。"""

        title @= "Order in which information is held"
        level @= INFORMATIVE
        detail @= "読み取り API は、この違いを吸収して、書いた順で返す（RDG_009）。"

    class SYN_015:
        """{{TERM_013}}は、デコレータ `@binds[<subject>](<implementation>, ...)` として、テストのクラス、または関数・メソッドの直前に書く。"""

        title @= "Writing the binding: binds"
        level @= MUST
        merge @= TERMS.TERM_013
        related @= INDEPENDENCE.IND_007

    class SYN_016:
        """`binds` には、型引数で{{TERM_002}}を指定しなければならない。型引数を省いた場合は、デコレータを適用する時点で `TypeError` とする。"""

        title @= "binds takes the subject type as a type argument"
        level @= MUST
        merge @= TERMS.TERM_002
        detail @= "型引数を省くと、型チェッカーが実装の適合を検査できない。検査しているように見えて、実際には検査されない書き方は、提供しない。"

    class SYN_017:
        """`binds` には、{{TERM_014}}を一つ以上渡せる。{{TERM_014}}は、対象型を作るもの（クラス、またはそれを返す関数）か、対象型そのもの（関数、module、オブジェクト）である。構築に必要な引数の有無は問わない。"""

        title @= "binds takes implementations: factories or objects"
        level @= MUST
        merge @= TERMS.TERM_014
        detail @= "関数一つを対象とする契約には関数そのものを、関数の集まりを対象とする契約には module そのものを渡す。実装が作るものか、そのものかは、実行時には区別しない。"
        related @= CONTRACT.CTR_012

    class SYN_018:
        """{{TERM_013}}は、付けた対象に適用する。テストのクラスに付けたときは、そのクラスの中のテストに適用する。クラスと、その中の関数・メソッドの両方に{{TERM_013}}が付いたときは、両方を適用する。モジュール全体への{{TERM_013}}は、当面提供しない。"""

        title @= "A binding applies to the decorated target"
        level @= MUST
        merge @= TERMS.TERM_013
        detail @= "関係語（SYN_010）と異なり、束縛はテストのクラスに付けられる。束縛は、どの実装に対するテストかを表す宣言であり、クラス単位が自然であるため。"

    class SYN_019:
        """`binds` の型注釈は、実装が{{TERM_002}}に{{TERM_015}}しないときに、型チェッカーが検出できるものでなければならない。"""

        title @= "A non-conforming implementation is detected by the type checker"
        level @= MUST
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_015
        detail @= "契約を持ち出して実装を作り直したとき、新しい実装が対象型に適合しているかを、実行前に知れる。適合の検査は、basedpyright と mypy で確認した。関数、module、ジェネリックな関数、オーバーロードされた関数を実装とする場合も同様である。"

    class SYN_020:
        """{{TERM_013}}は宣言であり、強制ではない。shikumi-contrace は、テストが束縛された実装を実際に使っているかを、検証しない。"""

        title @= "A binding is a declaration, not an enforcement"
        level @= INFORMATIVE
        merge @= TERMS.TERM_013

    class SYN_021:
        """`@=` 形式の記述器は、値の検査を、`@=` を評価する時点で行わなければならない。クラスの生成時に行う処理の中で、例外を出してはならない。"""

        title @= "Values of @= descriptors are checked when @= is evaluated"
        level @= MUST
        detail @= "Python 3.11 では、クラスの生成時に行う処理の中で出た例外が、`RuntimeError` に包まれ、原因が分かりにくくなる。Python 3.12 以降では、元の例外がそのまま出る。"

    class SYN_022:
        """利用者は、metamk の `Mk` を `Phase` という名前で、`phase_of` を同名で、`shikumi_contrace` から import して使える。"""

        title @= "metamk phase names can be imported from shikumi_contrace"
        level @= MUST
        detail @= "例えば、`from shikumi_contrace import Phase` と書ける。`Phase` は `from metamk import Mk` で得るものと同じオブジェクトを指す。"

    class SYN_023:
        """再エクスポートは、明示的な alias または `__all__` で公開名を示すことが望ましい。"""

        title @= "Re-exports are written in the explicit form"
        level @= SHOULD
        detail @= "例えば `from metamk import Mk as Phase` と書く。型チェッカーによっては、明示のない再エクスポートを公開名として扱わない（mypy の `--no-implicit-reexport` など）。"

    class SYN_024:
        """`@=` 形式の記述器は、`@=` の結果の型を、記述器自身の型として注釈しなければならない。"""

        title @= "The result of @= is annotated as the descriptor itself"
        level @= MUST
        detail @= "クラス本体の `name @= value` は、名前 `name` への代入であり、mypy は、結果の型が `name` の型と違うと、すべての行に誤りを出す。結果を記述器自身の型（`Self`）と注釈すれば、basedpyright と mypy の両方が受け入れる。実行時には、Shikumi が、クラスの生成時に取り除く、一時的な束縛が返る。"

    class SYN_025:
        """{{TERM_022}}は、記述器 `depends_on` を用い、依存元の{{TERM_001}}のクラス本体に `depends_on @= <contract>` と書く。依存先は、別の契約のクラスそのものへの参照でなければならず、文字列であってはならない。複数の依存先は、`depends_on @= ...` を複数回、書いた順に記述する。"""

        title @= "Writing contract dependencies: depends_on"
        level @= MUST
        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_022
        related @= CONTRACT.CTR_014
        detail @= "クラスそのものへの参照だけを受け取るため、通常の記述では、まだ定義されていない契約への forward reference は作らない。循環は検証でも診断する。"

    class SYN_026:
        """{{TERM_023}}は、記述器 `on_violation` を用い、{{TERM_006}}の条項のクラス本体に `on_violation @= <behavior>` と書く。標準値は `OUT_OF_SCOPE` と `REJECTED` である。独自の{{TERM_023}}は `define.violation(<name>)` で作る。"""

        title @= "Writing precondition violation behavior: on_violation"
        level @= MUST
        merge @= TERMS.TERM_006
        merge @= TERMS.TERM_023
        related @= CONTRACT.CTR_016
        detail @= "`on_violation` は、違反時の実装手段を指定しない。`REJECTED` であっても、例外を投げることや `pytest.raises` を使うことを意味しない。"

    class SYN_027:
        """`binds` の型引数には、{{TERM_002}}のクラスそのものに加えて、総称型のクラスに型引数を与えたもの（`Subject[Handle]`）を渡せる。{{TERM_013}}が記録するのは、型引数を与える前のクラス（`Subject`）である。契約の側は、型引数を与えないクラスを `subject @= Subject` と書く。"""

        title @= "binds accepts a generic subject given type arguments"
        level @= MUST
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_013
        related @= INDEPENDENCE.IND_006
        detail @= "実装が自分の型の値を返し、別のメソッドがその値を受け取る場合（予約を返す `reserve` と、予約を受け取る `release` など）、契約は、その型を型変数にした総称の Protocol で、「返したものを受け取る」という関係を、実装の型を契約へ持ち込まずに書ける。束縛で `@binds[Inventory[Reservation]](Impl)` と書くと、型チェッカーは、型引数を含めて適合を検査する（basedpyright と mypy で確認した）。型引数は型検査のためだけにあり、束縛には記録しない。読み取りは、型引数を与える前のクラスを返す。型引数を与えない総称型のクラスも、実行時には受理する。型チェッカーの設定によっては、型引数がないことを警告する。型引数は、クラスに対してだけ与えられる。ユニオン（`A | B`）や `Annotated` などは、対象型として受理せず、`TypeError` とする（SYN_016）。"
