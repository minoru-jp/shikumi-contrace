"""標準語彙の仕様。shikumi-contrace が標準として用意する語と、その意味。"""

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

from devdocs.canonical_sources.specification.contract import (
    SPECIFICATION_PART as CONTRACT,
)
from devdocs.canonical_sources.specification.vocab import SPECIFICATION_PART as VOCAB
from devdocs.canonical_sources.vocabulary import TERMS


@summary("標準の条項種別、違反時の扱い、関係語、注釈語と、その意味。")
@canonical_source(
    "標準語彙",
    filename="standard_vocabulary.md",
    order=55,
    merge_policy="local",
    heading="identity",
)
class SPECIFICATION_PART:
    """shikumi-contrace が標準として用意する語を定める。語は、少数の開いた情報型（条項種別、違反時の扱い、関係、注釈）の値であり、独自語彙も同じ生成器で作れる。標準の語の識別子は英語で、日本語名を括弧に併記する。"""

    class STD_001:
        """標準の{{TERM_005}} `PRE`（事前条件）は、{{TERM_006}}の条項を表す。"""

        title @= "Clause kind: PRE"
        level @= MUST
        merge @= TERMS.TERM_005
        merge @= TERMS.TERM_006
        detail @= "置く位置の規則は、契約の構造の仕様に定める。"
        related @= CONTRACT.CTR_009

    class STD_002:
        """標準の{{TERM_005}} `POST`（事後条件）は、{{TERM_007}}の条項を表す。"""

        title @= "Clause kind: POST"
        level @= MUST
        merge @= TERMS.TERM_005
        merge @= TERMS.TERM_007
        detail @= "置く位置の規則は、契約の構造の仕様に定める。"
        related @= CONTRACT.CTR_009

    class STD_003:
        """標準の{{TERM_005}} `INV`（不変条件）は、{{TERM_008}}の条項を表す。"""

        title @= "Clause kind: INV"
        level @= MUST
        merge @= TERMS.TERM_005
        merge @= TERMS.TERM_008
        detail @= "置く位置の規則は、契約の構造の仕様に定める。"
        related @= CONTRACT.CTR_009

    class STD_004:
        """標準の{{TERM_023}} `OUT_OF_SCOPE`（契約外）は、その事前条件を満たさない呼び出しについて、その条項が振る舞いを約束しないことを表す。"""

        title @= "Violation behavior: OUT_OF_SCOPE"
        level @= MUST
        merge @= TERMS.TERM_023
        detail @= "上流で必ず検査されることや、実装が何もしないことを意味しない。単に、違反した呼び出しの振る舞いを、この条項の約束に含めない。"
        related @= CONTRACT.CTR_016

    class STD_005:
        """標準の{{TERM_023}} `REJECTED`（拒否）は、その事前条件を満たさない呼び出しを、実装が正常な成功として受理しないことまで、その条項が約束することを表す。"""

        title @= "Violation behavior: REJECTED"
        level @= MUST
        merge @= TERMS.TERM_023
        detail @= "拒否の実現方法は規定しない。例外、失敗を表す戻り値、プロトコル上の応答などでよく、特定のガード節やテスト構文を要求しない。"
        related @= CONTRACT.CTR_016

    class STD_010:
        """標準の{{TERM_019}} `upholds`（守る）は、その条項が効いている場面で、条項が守られること、成り立つことを、テストが確かめることを表す。"""

        title @= "Relation word: upholds"
        level @= MUST
        merge @= TERMS.TERM_019
        detail @= "事前条件に対しては、条件を満たす入力（境界を含む）が受理されること、事後条件に対しては、事後条件が成り立つこと、不変条件に対しては、不変条件が保たれることを確かめる。"
        related @= VOCAB.VOC_001

    class STD_011:
        """標準の{{TERM_019}} `violates`（破る）は、その条項をわざと破る場面を作り、そのときの振る舞いを、テストが確かめることを表す。"""

        title @= "Relation word: violates"
        level @= MUST
        merge @= TERMS.TERM_019
        detail @= (
            "主に事前条件に対して使う。事後条件と不変条件に対しては、通常は使わない。"
        )
        related @= VOCAB.VOC_001

    class STD_012:
        """標準の{{TERM_019}}は、条項に対するテストの姿勢だけを表さなければならない。条項の種別を表してはならない。"""

        title @= "Relation words express only the stance"
        level @= MUST_NOT
        merge @= TERMS.TERM_019
        detail @= "条項の種別は、条項自身が持つ。関係語で繰り返すと、同じ情報を二か所で保守することになる。種別を含む語（例えば `preserves`）が必要な利用者は、独自語彙として定義できる。"
        related @= VOCAB.VOC_001

    class STD_013:
        """標準の{{TERM_019}}と{{TERM_005}}の組み合わせは、次のとおり用いる。

        | 条項種別 | `upholds` | `violates` |
        | --- | --- | --- |
        | `PRE` | 条件を満たす入力（境界を含む）が受理される | 条件を破った呼び出しで、違反時の振る舞いを確かめる |
        | `POST` | 事後条件が成り立つ | 通常は使わない |
        | `INV` | 不変条件が保たれる | 通常は使わない |
        """

        title @= "How relation words combine with clause kinds"
        level @= INFORMATIVE
        merge @= TERMS.TERM_005
        merge @= TERMS.TERM_019
        detail @= "通常は使わない組み合わせの診断は、検証規則に定める（REG_019）。"
        related @= VOCAB.VOC_001

    class STD_020:
        """標準の{{TERM_020}} `note`（補足）は、補足全般を表す。既定の注釈語である。"""

        title @= "Annotation word: note"
        level @= MUST
        merge @= TERMS.TERM_020
        detail @= "観点: 説明。主な位置: 全て。"
        related @= VOCAB.VOC_001

    class STD_021:
        """標準の{{TERM_020}} `rationale`（理由）は、その約束がある理由を表す。"""

        title @= "Annotation word: rationale"
        level @= MUST
        merge @= TERMS.TERM_020
        detail @= "観点: 説明。主な位置: 契約、メンバー、条項。契約を別の実装へ持ち出したときに、最も失われやすい情報である。"
        related @= VOCAB.VOC_001

    class STD_022:
        """標準の{{TERM_020}} `caution`（注意）は、誤解しやすい点、破ると影響が大きい点を表す。"""

        title @= "Annotation word: caution"
        level @= MUST
        merge @= TERMS.TERM_020
        detail @= "観点: 説明。主な位置: 全て。変更の際の落とし穴を、先に伝える。"
        related @= VOCAB.VOC_001

    class STD_023:
        """標準の{{TERM_020}} `example`（例）は、入力と結果の具体例を表す。"""

        title @= "Annotation word: example"
        level @= MUST
        merge @= TERMS.TERM_020
        detail @= "観点: 説明。主な位置: 条項。条項文の意味を具体化する。例が実際の振る舞いとずれないよう、テストで確かめることが望ましい。"
        related @= VOCAB.VOC_001

    class STD_024:
        """標準の{{TERM_020}} `source`（出典）は、要件、issue、RFC など、上流への参照を表す。"""

        title @= "Annotation word: source"
        level @= MUST
        merge @= TERMS.TERM_020
        detail @= "観点: 説明。主な位置: 契約、条項、テスト。"
        related @= VOCAB.VOC_001

    class STD_025:
        """標準の{{TERM_020}} `assumption`（前提）は、契約が保証せず、前提としていることを表す。例えば、単一のスレッドで使われること。"""

        title @= "Annotation word: assumption"
        level @= MUST
        merge @= TERMS.TERM_020
        detail @= "観点: 説明。主な位置: 契約、メンバー。別の環境へ契約を持ち出すときに、再確認すべき前提の一覧になる。"
        related @= VOCAB.VOC_001

    class STD_026:
        """標準の{{TERM_020}} `security`（セキュリティ）は、守るべき性質（セキュリティ）に関わることを示す目印である。"""

        title @= "Annotation word: security"
        level @= MUST
        merge @= TERMS.TERM_020
        detail @= "観点: 領域。主な位置: 契約、メンバー、条項、テスト。作り直しで必ず引き継ぐ対象と、条項を弱める変更の前に確認する対象を示す。付いていないことは、安全に関係しないことを保証しない。注釈の文に、攻撃の具体的な手順を書かないことが望ましい。文は任意である。"
        related @= VOCAB.VOC_001

    class STD_027:
        """標準の{{TERM_020}} `performance`（性能）は、時間や空間の制約に関わることを示す目印である。"""

        title @= "Annotation word: performance"
        level @= MUST
        merge @= TERMS.TERM_020
        detail @= "観点: 領域。主な位置: 条項、テスト。"
        related @= VOCAB.VOC_001

    class STD_028:
        """標準の{{TERM_020}} `concurrency`（並行性）は、並行性や原子性に関わることを示す目印である。"""

        title @= "Annotation word: concurrency"
        level @= MUST
        merge @= TERMS.TERM_020
        detail @= (
            "観点: 領域。主な位置: 条項、テスト。崩れやすく、確かめにくい箇所を示す。"
        )
        related @= VOCAB.VOC_001

    class STD_029:
        """標準の{{TERM_020}} `critical`（重大）は、違反の影響が大きいことを示す目印である。"""

        title @= "Annotation word: critical"
        level @= MUST
        merge @= TERMS.TERM_020
        detail @= "観点: 重さ。主な位置: 条項、テスト。失敗の優先順位と、弱める変更の前に確認する対象を示す。文は任意である。"
        related @= VOCAB.VOC_001

    class STD_030:
        """標準の{{TERM_020}} `todo`（未対応）は、未対応であること、一時的であることを示す。"""

        title @= "Annotation word: todo"
        level @= MUST
        merge @= TERMS.TERM_020
        detail @= "観点: 状態。主な位置: 全て。"
        related @= VOCAB.VOC_001

    class STD_031:
        """標準の{{TERM_020}} `provisional`（暫定）は、内容自体が未確定であることを示す。"""

        title @= "Annotation word: provisional"
        level @= MUST
        merge @= TERMS.TERM_020
        detail @= "観点: 状態。主な位置: 契約、メンバー、条項。固めてよい条項と区別する。`todo` はやることが残っていること、`provisional` は内容が未確定であることを表す。"
        related @= VOCAB.VOC_001

    class STD_032:
        """標準の{{TERM_020}} `legacy`（互換）は、互換性のために維持している振る舞いであることを示す。望ましい設計とは限らない。"""

        title @= "Annotation word: legacy"
        level @= MUST
        merge @= TERMS.TERM_020
        detail @= "観点: 状態。主な位置: 条項、テスト。作り直しのとき、引き継ぐかを判断する対象を示し、整理の対象として扱われることを防ぐ。"
        related @= VOCAB.VOC_001

    class STD_033:
        """標準の{{TERM_020}} `deprecated`（廃止予定）は、削除が決まっていることを示す。"""

        title @= "Annotation word: deprecated"
        level @= MUST
        merge @= TERMS.TERM_020
        detail @= "観点: 状態。主な位置: 条項、テスト。作り直しのとき、引き継がない対象を示す。`legacy` は引き継ぐかを判断する対象、`deprecated` は引き継がない対象である。"
        related @= VOCAB.VOC_001

    class STD_034:
        """標準の{{TERM_020}} `manual`（手動確認）は、自動テストではなく、手動や別の手段で確認する条項であることを示す。"""

        title @= "Annotation word: manual"
        level @= MUST
        merge @= TERMS.TERM_020
        detail @= "観点: 検証。主な位置: 条項。意図して自動テストを持たない条項と、テストの書き忘れを区別する。"
        related @= VOCAB.VOC_001

    class STD_035:
        """標準の{{TERM_020}} `boundary`（境界）は、境界値を扱うテストであることを示す。"""

        title @= "Annotation word: boundary"
        level @= MUST
        merge @= TERMS.TERM_020
        detail @= "観点: 検証。主な位置: テスト。"
        related @= VOCAB.VOC_001

    class STD_036:
        """標準の{{TERM_020}} `regression`（回帰）は、過去の不具合の再発を防ぐテストであることを示す。"""

        title @= "Annotation word: regression"
        level @= MUST
        merge @= TERMS.TERM_020
        detail @= "観点: 検証。主な位置: テスト。消してよいテストではないことを、後から変更する人と LLM に伝える。"
        related @= VOCAB.VOC_001

    class STD_040:
        """注釈の文は、任意でなければならない。`security` や `critical` のように、語だけで意味が足りる{{TERM_020}}は、文を伴わずに付けられなければならない。"""

        title @= "The text of an annotation is optional"
        level @= MUST
        merge @= TERMS.TERM_020
        related @= VOCAB.VOC_001

    class STD_041:
        """標準の{{TERM_020}}は、契約、メンバー、条項、テストのいずれにも付けられなければならない。各語に挙げる主な位置は目安であり、制限ではない。"""

        title @= "Annotation words are not restricted by position"
        level @= MUST
        merge @= TERMS.TERM_020
        related @= VOCAB.VOC_001

    class STD_042:
        """標準語彙の識別子は、英語とする。日本語名は、この文書の各項目に併記する。独自語彙の名前は、言語を問わない。"""

        title @= "Identifiers of the standard vocabulary are in English"
        level @= MUST
        related @= VOCAB.VOC_001
