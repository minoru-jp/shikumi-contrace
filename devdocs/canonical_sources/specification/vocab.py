"""語彙の仕様。標準語彙と独自語彙の関係。"""

from shikumi_devdoc.fields.specification import (
    INFORMATIVE,
    MAY,
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


@summary("標準語彙の提供と、独自語彙を妨げないこと、未知の語彙を拒否しないこと。")
@canonical_source(
    "語彙",
    filename="vocab.md",
    order=50,
    merge_policy="local",
    heading="identity",
)
class SPECIFICATION_PART:
    """条項種別、関係づけの語、注釈の語などの語彙について、shikumi-contrace が用意するものと、利用者に委ねるものを定める。語彙は自由であるほどよい。表記ゆれは表現力の一部として受け入れる。"""

    class VOC_001:
        """shikumi-contrace は{{TERM_011}}を提供しなければならない。{{TERM_011}}は、{{TERM_005}}、{{TERM_023}}、{{TERM_019}}、{{TERM_020}}を含む。"""

        title @= "A standard vocabulary is provided"
        level @= MUST
        merge @= TERMS.TERM_005
        merge @= TERMS.TERM_011
        merge @= TERMS.TERM_023
        merge @= TERMS.TERM_019
        merge @= TERMS.TERM_020
        detail @= "標準の語とその意味は、標準語彙の仕様書に定める。"
        related @= AIM.AIM_006

    class VOC_002:
        """shikumi-contrace は、利用者が{{TERM_012}}を定義して使うことを妨げてはならない。"""

        title @= "Custom vocabulary is not obstructed"
        level @= MUST_NOT
        merge @= TERMS.TERM_012
        related @= AIM.AIM_006

    class VOC_003:
        """{{TERM_012}}は、{{TERM_011}}と同じ位置で、同じ記述方法で使えなければならない。"""

        title @= "Custom vocabulary is used the same way as the standard one"
        level @= MUST
        merge @= TERMS.TERM_011
        merge @= TERMS.TERM_012

    class VOC_004:
        """shikumi-contrace は、語彙が{{TERM_011}}に含まれないことを理由に、診断情報を出してはならない。未知の語彙を拒否してはならない。"""

        title @= "Unknown vocabulary is not rejected"
        level @= MUST_NOT
        merge @= TERMS.TERM_011
        detail @= "ここでいう拒否には、エラーだけでなく、警告も含む。語彙の取り扱いに関する診断は、利用者が自らの規定として追加した検証規則だけが出す。"

    class VOC_005:
        """shikumi-contrace は、語彙の表記ゆれを統一したり、拒否したりしてはならない。"""

        title @= "Variations in spelling are accepted"
        level @= MUST_NOT
        detail @= "表記ゆれは、あって当たり前のものである。同じ意味を別の語で書けることは、表現力を上げる。"

    class VOC_006:
        """利用者は、自らの規定として語彙を制限する検証規則を、shikumi-contrace の外で定義してよい。shikumi-contrace の既定では、語彙を制限しない。"""

        title @= "Restricting vocabulary is the user's choice"
        level @= MAY

    class VOC_007:
        """{{TERM_009}}の語彙にも、VOC_002 から VOC_005 までの規則を同様に適用する。"""

        title @= "Note vocabulary follows the same rules"
        level @= MUST
        merge @= TERMS.TERM_009

    class VOC_008:
        """語彙は、shikumi-contrace が定義する開いた情報型（条項種別、違反時の扱い、関係、注釈）の値として表さなければならない。{{TERM_011}}も{{TERM_012}}も、同じ生成器で作る値でなければならず、{{TERM_012}}を使うために、情報型を登録する必要があってはならない。"""

        title @= "Vocabulary is represented as values of open information types"
        level @= MUST
        merge @= TERMS.TERM_011
        merge @= TERMS.TERM_012
        merge @= TERMS.TERM_023
        detail @= "語を情報型として登録させると、登録のない語が意味像に現れず、語彙の自由が実質的に失われる。語を値にすれば、語彙の数にかかわらず、認識する情報型は少数に保てる。"

    class VOC_009:
        """{{TERM_012}}は、意味像において、{{TERM_011}}と並んで現れなければならない。"""

        title @= "Custom vocabulary appears in the semantic view like the standard one"
        level @= MUST
        merge @= TERMS.TERM_011
        merge @= TERMS.TERM_012

    class VOC_010:
        """{{TERM_023}}を、意図して決めずに残したいときは、プロジェクトが{{TERM_012}}の{{TERM_023}}（例: `UNDECIDED = define.violation("undecided")`）を定義して使ってよい。{{TERM_023}}の省略は、宣言していないことを表し、意図した保留とは区別できる。"""

        title @= "Guidance: marking violation behavior as deliberately undecided"
        level @= INFORMATIVE
        merge @= TERMS.TERM_012
        merge @= TERMS.TERM_023
        detail @= "違反時の扱いは、四つの状態を区別して読める。`REJECTED` は、違反した呼び出しを正常な成功として受理しないことまで約束する。`OUT_OF_SCOPE` は、違反時の振る舞いを約束に含めない。プロジェクトの語（`UNDECIDED` など）は、意図して未決定であることを表す。省略は、宣言していないこと（書き忘れの可能性）を表す。読み取りでは、`on_violation` が省略された事前条件は `clauses_of` を絞り込んで一覧できる。省略を許さないプロジェクトは、自らの規定として、この絞り込みを自分のテストで検査できる（VOC_006）。shikumi-contrace は、省略を診断しない。省略は正当な書き方であり、診断にすると宣言が事実上の義務になる（REG_022）。多くのプロジェクトが同じ語を必要とするようになれば、標準の語への追加を検討する。"
