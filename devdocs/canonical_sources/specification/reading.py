"""情報の読み取りの仕様。宣言された契約とテストの情報を、本体が読み取る API。"""

from shikumi_devdoc.fields.specification import (
    INFORMATIVE,
    MUST,
    MUST_NOT,
    detail,
    level,
    related,
)
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import title

from devdocs.canonical_sources.specification.aim import SPECIFICATION_PART as AIM
from devdocs.canonical_sources.vocabulary import TERMS


@summary(
    "宣言された契約とテストの情報を読み取る、テストランナーに依存しない API。条項とテストの対応の追跡。"
)
@canonical_source(
    "情報の読み取り",
    filename="reading.md",
    order=47,
    merge_policy="local",
    heading="identity",
)
class SPECIFICATION_PART:
    """条項とテストの対応を追えるようにするため、宣言された情報を読み取る API を定める。pytest 連携は必要最小限に留めるため、絞り込みや一覧などは、この API を用いて、利用者が書ける。API の名前は、公開 API の名前と配置の仕様に定める。"""

    class RDG_001:
        """{{TERM_017}}は、宣言された契約とテストの情報を読み取る API を提供しなければならない。この API は、特定のテストランナーに依存してはならない。"""

        title @= "A reading API independent of any test runner"
        level @= MUST
        merge @= TERMS.TERM_017
        related @= AIM.AIM_003

    class RDG_002:
        """読み取り API は、テストが持つ{{TERM_010}}（{{TERM_019}}と{{TERM_004}}）、注釈、{{TERM_013}}を読めなければならない。"""

        title @= "Reading what a test declares"
        level @= MUST
        merge @= TERMS.TERM_004
        merge @= TERMS.TERM_010
        merge @= TERMS.TERM_013
        merge @= TERMS.TERM_019
        detail @= "テストのクラスに付けた束縛も、そのクラスの中のテストの束縛として読める（SYN_018）。関数のオブジェクトからクラスを辿るのは、`__qualname__` による解決で、モジュール直下のクラスに限る。インスタンスのメソッドからは、インスタンスのクラスを辿れるので、関数の中で定義したクラスも読める。関数の中で定義したクラスの、関数のオブジェクトからは辿れない。pytest 連携は、収集したクラスから直接読むので、影響しない。"

    class RDG_003:
        """読み取り API は、{{TERM_001}}が持つ{{TERM_004}}の一覧（種別、{{TERM_023}}、条項文、注釈を含む）を、契約から読めなければならない。"""

        title @= "Reading the clauses of a contract"
        level @= MUST
        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_004
        merge @= TERMS.TERM_023

    class RDG_004:
        """読み取り API は、{{TERM_004}}から、その条項に{{TERM_010}}したテストを逆引きできなければならない。逆引きは、利用者が渡したテストの範囲で行う。"""

        title @= "Looking up the tests related to a clause"
        level @= MUST
        merge @= TERMS.TERM_004
        merge @= TERMS.TERM_010
        related @= AIM.AIM_001

    class RDG_005:
        """読み取り API は、{{TERM_010}}を持つテストのない{{TERM_004}}を、一覧できなければならない。"""

        title @= "Listing clauses that no test is related to"
        level @= MUST
        merge @= TERMS.TERM_004
        merge @= TERMS.TERM_010
        merge @= TERMS.TERM_023
        detail @= "この一覧は、記録された関係づけの有無だけを示す。条項の種別、違反時の扱い、その他の意味から、その条項にテストが必要かどうかを推論しない。"
        related @= AIM.AIM_001

    class RDG_006:
        """読み取り API は、情報を読むだけでなければならない。契約やテストの内容を書き換えてはならない。"""

        title @= "The reading API only reads"
        level @= MUST_NOT

    class RDG_007:
        """読み取り API は、デコレータが包んだ関数について、`__wrapped__` の連鎖をたどって、内側の関数に付いた情報も読まなければならない。外側と内側の両方に付いた情報は、両方を返す。"""

        title @= "The reading API follows the __wrapped__ chain"
        level @= MUST
        detail @= "情報は、オブジェクトの同一性に付く。宣言が、他のデコレータ（`functools.wraps` を使うものや `mock.patch` など）より内側にあると、情報は内側の関数に付き、外側のラッパー関数には付かない。連鎖をたどらないと、そのような宣言を読み落とす。"

    class RDG_008:
        """テストの関数とメソッドは、Shikumi の実体として扱わない。テストの情報は、関数やメソッドのオブジェクトから、直接読む。"""

        title @= "Test functions are read directly, not as Shikumi entities"
        level @= INFORMATIVE
        detail @= "Shikumi の標準の構造は、クラスを実体として扱い、関数とメソッドを実体として扱わない。契約の側（クラス）の検証には、Shikumi の検証の枠組みを用いるが、テストの側の情報は、読み取り API で読む。テストの側に関わる検証規則（REG_010 など）も、読み取り API を用いて実装できる。"

    class RDG_009:
        """読み取り API は、情報を、書いた順に返さなければならない。同じ対象にデコレータで付けた情報は、上から下の順に、クラスの本体の `@=` で付けた情報は、デコレータで付けた情報の後に、書いた順に返す。外側のラッパーの情報は、内側の関数の情報より先に返す。"""

        title @= "Information is returned in the order it was written"
        level @= MUST
        detail @= "デコレータは、下から適用されるため、付けた情報の保持の順は、書いた順の逆になる（SYN_014）。読み取り API が、これを吸収する。"

    class RDG_010:
        """読み取り API は、{{TERM_001}}から、その契約が直接依存する契約を、書いた順で読めなければならない。また、利用者が渡した範囲の中で、ある契約に直接依存する契約を逆引きできなければならない。逆方向の関係は保存せず、宣言された一方向の{{TERM_022}}から求める。"""

        title @= "Reading contract dependencies in both directions"
        level @= MUST
        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_022
        related @= AIM.AIM_003
