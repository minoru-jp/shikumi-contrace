"""テスト側の記述の仕様。テストを契約の条項に関係づける記述。"""

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
from devdocs.canonical_sources.specification.contract import (
    SPECIFICATION_PART as CONTRACT,
)
from devdocs.canonical_sources.specification.independence import (
    SPECIFICATION_PART as INDEPENDENCE,
)
from devdocs.canonical_sources.vocabulary import TERMS


@summary("テストを契約の条項に関係づける記述、注釈、束縛。")
@canonical_source(
    "テスト側の記述",
    filename="test_side.md",
    order=40,
    merge_policy="local",
    heading="identity",
)
class SPECIFICATION_PART:
    """テストが、契約のどの条項に対して何をするのかを、テストの直前に宣言する記述を定める。条項の文は契約の側に一度だけ書き、テストはそれを参照する。"""

    class TST_001:
        """テストは、テストランナーが収集する通常の関数またはメソッドでなければならない。shikumi-contrace はテストの形を変えない。"""

        title @= "Tests remain ordinary tests of the test runner"
        level @= MUST
        related @= AIM.AIM_003

    class TST_002:
        """テストは、契約の{{TERM_004}}に対する{{TERM_010}}を、テストの直前に宣言できなければならない。{{TERM_010}}は、対象の条項を、契約の実体そのものへの参照として指さなければならない。文字列で指してはならない。"""

        title @= "A test declares its relation to clauses, by reference"
        level @= MUST
        merge @= TERMS.TERM_004
        merge @= TERMS.TERM_010
        related @= CONTRACT.CTR_004

    class TST_003:
        """一つのテストは、複数の{{TERM_004}}に関係づけられてよい。"""

        title @= "One test may relate to several clauses"
        level @= MAY
        merge @= TERMS.TERM_004
        detail @= "契約に基づくテストでは、一回の実行が、一つの事前条件の違反の拒否と、一つの不変条件の保持を同時に確かめることがある。"

    class TST_004:
        """{{TERM_010}}は、条項に対するテストの姿勢を表す{{TERM_019}}を伴わなければならない。標準の{{TERM_019}}は、`upholds`（守る）と `violates`（破る）である。"""

        title @= "A relation carries a relation word"
        level @= MUST
        merge @= TERMS.TERM_010
        merge @= TERMS.TERM_019
        detail @= "標準の関係語の意味は、標準語彙の仕様書に定める。"

    class TST_005:
        """テストには、{{TERM_009}}を付けてよい。"""

        title @= "Notes may be attached to a test"
        level @= MAY
        merge @= TERMS.TERM_009
        detail @= "条項やテスト名からは読み取れない、判断の理由、境界の意図、注意事項を、後からテストを読む人と LLM に伝えるために用いる。"

    class TST_006:
        """条項文は、契約の側に一度だけ書き、テストの側で繰り返さないことが望ましい。テスト名は、そのテストが確かめる具体的な振る舞いを表すことが望ましい。"""

        title @= "Clause statements are not repeated on the test side"
        level @= SHOULD
        detail @= "テスト名と条項名が重なると、同じ文を二か所で保守することになる。条項文は契約に、具体的な振る舞いはテスト名に、それぞれ分けて置く。"
        related @= CONTRACT.CTR_011

    class TST_007:
        """契約の{{TERM_002}}と{{TERM_014}}を結び付ける{{TERM_013}}は、テストの側に記述しなければならない。"""

        title @= "Bindings are written on the test side"
        level @= MUST
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_013
        merge @= TERMS.TERM_014
        related @= INDEPENDENCE.IND_007
        detail @= "束縛の書式は、記述器と書式の仕様に定める。"

    class TST_008:
        """テストの本体の内側の構造は、この仕様の範囲外であり、shikumi-contrace は規定しない。"""

        title @= "The inside of a test body is out of scope"
        level @= INFORMATIVE
        related @= AIM.AIM_008
