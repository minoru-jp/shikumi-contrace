"""契約の構造の仕様。契約がどのような実体で構成されるか。"""

from shikumi_devdoc.fields.specification import (
    INFORMATIVE,
    MAY,
    MUST,
    SHOULD,
    detail,
    level,
    related,
)
from shikumi_devdoc.norms.common import canonical_source, merge, summary
from shikumi_devdoc.norms.document import title

from devdocs.canonical_sources.specification.aim import SPECIFICATION_PART as AIM
from devdocs.canonical_sources.vocabulary import TERMS


@summary("契約を構成する実体（対象型、メンバー、条項）と、その位置の規則。")
@canonical_source(
    "契約の構造",
    filename="contract.md",
    order=20,
    merge_policy="local",
    heading="identity",
)
class SPECIFICATION_PART:
    """契約を、対象型、メンバー、条項というクラスの入れ子として記述するときの構造を定める。Shikumi が扱う粒度はクラスまでであるため、メソッド単位の条項もクラスで表す。"""

    class CTR_001:
        """{{TERM_001}}は、{{TERM_002}}の指定と{{TERM_004}}を含む、Python のクラスとして記述されなければならない。"""

        title @= "A contract is a class"
        level @= MUST
        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_004
        related @= AIM.AIM_001

    class CTR_002:
        """一つの{{TERM_001}}は、一つの{{TERM_002}}を、その型そのものへの参照として指定しなければならない。文字列による指定であってはならない。"""

        title @= "A contract names one subject type by reference"
        level @= MUST
        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_002
        detail @= "対象型を文字列で指すと、契約が必要以上に汎化され、IDE から辿ることもできなくなる。契約は型を保ったまま記述する。"

    class CTR_003:
        """契約が定義する型は、構造的な型（Protocol）でなければならない。dataclass などの具象クラスを契約に置いてはならない。"""

        title @= "Types defined by a contract are structural"
        level @= MUST
        detail @= "実装が契約を import せず、自前の型を持ったまま、構造的に適合できるようにするため。値を表す型も、必要な属性を読み取り専用のプロパティとして持つ構造的な型で表す。"
        related @= AIM.AIM_001

    class CTR_004:
        """{{TERM_004}}は、契約または{{TERM_003}}の中に入れ子にしたクラスとして記述し、クラスの docstring を条項文としなければならない。一つの条項は、一つの約束を一文で述べる。"""

        title @= "A clause is a nested class whose docstring is the clause statement"
        level @= MUST
        merge @= TERMS.TERM_003
        merge @= TERMS.TERM_004

    class CTR_005:
        """{{TERM_002}}全体に対する条項は、契約の直下に置かなければならない。"""

        title @= "Clauses about the whole subject type sit directly under the contract"
        level @= MUST
        merge @= TERMS.TERM_002

    class CTR_006:
        """{{TERM_003}}は、{{TERM_002}}のメソッドなどを表す、契約の直下の入れ子クラスとして記述し、そのメンバーに対する条項は、メンバーのクラスの中に置かなければならない。{{TERM_002}}が呼び出し可能な型である場合は、CTR_012 に従ってもよい。"""

        title @= "A member is a nested class that holds the clauses of one method"
        level @= MUST
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_003
        detail @= "Shikumi は、クラスより細かい粒度であるメソッドを実体として扱わない。そのため、メソッド単位の条項も、メソッドを表すクラスを介して表す。"

    class CTR_007:
        """{{TERM_003}}は、{{TERM_002}}のどのメンバーを表すかを、対象型のそのメンバーへの参照として指定しなければならない。"""

        title @= "A member refers to the member of the subject type"
        level @= MUST
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_003

    class CTR_008:
        """{{TERM_003}}のクラス名は、参照先の対象型のメンバー名と一致していることが望ましい。一致しない場合は診断する。ただし、対象型の指定とメンバーの指定を同時に持つ契約（CTR_012）は、この規則の対象としない。"""

        title @= "Member class names follow the referred member names"
        level @= SHOULD
        merge @= TERMS.TERM_003
        detail @= "IDE のリネームで、参照先の名前だけが変わったときのずれを検出するための保険になる。"

    class CTR_009:
        """標準語彙の{{TERM_006}}と{{TERM_007}}は、{{TERM_003}}を表す実体（メンバーのクラス、または CTR_012 により `member` を持つ契約）の直下に置かなければならない。標準語彙の{{TERM_008}}は、{{TERM_002}}の指定を持つ契約の直下に置かなければならない。置く位置が異なる場合は診断する。{{TERM_012}}の{{TERM_005}}は、この位置の規則の対象としない。"""

        title @= "Standard clause kinds have fixed positions"
        level @= MUST
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_003
        merge @= TERMS.TERM_005
        merge @= TERMS.TERM_006
        merge @= TERMS.TERM_007
        merge @= TERMS.TERM_008
        merge @= TERMS.TERM_012
        detail @= "位置には役割を与え、そこに入れる言葉は縛らない。位置の規則は標準語彙にだけ適用し、独自語彙は妨げない。契約が対象型の指定とメンバーの指定の両方を持つ場合は、事前条件、事後条件、不変条件のいずれも、契約の直下に置ける。"

    class CTR_010:
        """{{TERM_009}}は、契約、メンバー、条項のいずれにも付けてよい。"""

        title @= "Notes may be attached to a contract, a member, or a clause"
        level @= MAY
        merge @= TERMS.TERM_009

    class CTR_011:
        """条項文は、その条項だけを読んで意味が分かるように書くことが望ましい。他の条項やテストを読まなければ意味が分からない書き方は避ける。"""

        title @= "A clause statement is readable on its own"
        level @= SHOULD

    class CTR_012:
        """{{TERM_002}}が呼び出し可能な型、すなわち `__call__` だけを持つ Protocol であるとき、契約のクラス自身が、その `__call__` を表してよい。そのためには、契約の本体に、対象型の指定に加えて、`member @= <subject>.__call__` を書く。このとき、{{TERM_003}}のクラスは要らず、{{TERM_006}}と{{TERM_007}}の条項を、契約の直下に置ける。"""

        title @= "A contract may itself stand for the single member of a callable subject type"
        level @= MAY
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_003
        merge @= TERMS.TERM_006
        merge @= TERMS.TERM_007
        detail @= "関数一つを対象とする契約は、`__call__` だけを持つ Protocol（callback protocol）を対象型にして書く。新しい記述器は要らない。"

    class CTR_013:
        """関数の集まり（module）を対象とする契約は、メソッドを持つ通常の{{TERM_002}}で書き、module は{{TERM_014}}として{{TERM_013}}する。"""

        title @= "A contract for a module of functions uses an ordinary subject type"
        level @= INFORMATIVE
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_013
        merge @= TERMS.TERM_014
        detail @= "module を束縛する書式は、記述器と書式の仕様に定める。"

    class CTR_014:
        """{{TERM_001}}は、一つ以上の別の{{TERM_001}}への{{TERM_022}}を持ってよい。`B` が `A` に依存するとは、`A` の変更または廃止によって、`B` の妥当性または存続意義を再評価する必要が生じることを表す。"""

        title @= "A contract may depend on other contracts"
        level @= MAY
        merge @= TERMS.TERM_001
        merge @= TERMS.TERM_022
        detail @= "依存は論理的な含意ではなく、変更の影響を追跡するための一方向の関係である。依存先の変更や廃止によって、依存元を自動的に変更または廃止しない。複数の依存先を持ってよい。"

    class CTR_015:
        """{{TERM_022}}は循環してはならない。直接の相互依存だけでなく、複数の契約を経由して依存元へ戻る依存も認めない。"""

        title @= "Contract dependencies are acyclic"
        level @= MUST
        merge @= TERMS.TERM_022

    class CTR_016:
        """{{TERM_006}}の条項は、{{TERM_023}}を持ってよい。{{TERM_023}}は、その事前条件を満たさない呼び出しについて、その条項自身がどこまでを約束の範囲に含めるかを表す。"""

        title @= "A precondition may declare how violation is treated"
        level @= MAY
        merge @= TERMS.TERM_006
        merge @= TERMS.TERM_023
        detail @= "違反時の扱いを書かないことは、`OUT_OF_SCOPE` を書いたこととは同じではない。省略は、違反時の扱いについて、この情報を宣言していないことを表す。"
