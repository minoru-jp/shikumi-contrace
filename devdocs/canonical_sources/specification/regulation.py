"""規定体と検証の仕様。shikumi-contrace が提供する検証規則。"""

from shikumi_devdoc.fields.specification import (
    INFORMATIVE,
    MAY,
    MUST,
    MUST_NOT,
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
from devdocs.canonical_sources.specification.pytest_integration import (
    SPECIFICATION_PART as PYTEST_INTEGRATION,
)
from devdocs.canonical_sources.specification.syntax import (
    SPECIFICATION_PART as SYNTAX,
)
from devdocs.canonical_sources.specification.vocab import (
    SPECIFICATION_PART as VOCAB,
)
from devdocs.canonical_sources.vocabulary import TERMS


@summary(
    "契約の構造と独立性を検査する検証規則、参照を制限する範囲の決め方、検査の性質および限界。"
)
@canonical_source(
    "規定体と検証",
    filename="regulation.md",
    order=60,
    merge_policy="local",
    heading="identity",
)
class SPECIFICATION_PART:
    """shikumi-contrace を Shikumi の規定体として構成するときに提供する検証規則と、その検査の性質を定める。検査は診断情報を返すだけで、契約やテストを書き換えない。"""

    class REG_001:
        """shikumi-contrace の契約とテスト向けの記述は、Shikumi の情報型、記述器、検証規則から成る規定体として定義しなければならない。"""

        title @= "The specification body is composed of information types, descriptors and validation rules"
        level @= MUST
        related @= AIM.AIM_007

    class REG_002:
        """検証は、Python の実行後に成立している実行時の状態に基づかなければならない。ソースコードを静的に解析してはならない。"""

        title @= "Validation is based on the runtime state after execution"
        level @= MUST
        detail @= "検査の対象は、import 後の module と package の名前空間、およびクラスの属性である。関数の本体の中で遅延して行われる import や、リストなどの内部の値までは検査しない。検査は信頼できる Python コードにのみ行う。import 時のコードは通常の権限で実行される。"

    class REG_003:
        """shikumi-contrace は、{{TERM_016}}が、テストおよび{{TERM_014}}を参照していないかを検査する検証規則を提供しなければならない。違反は診断情報として報告する。"""

        title @= "A rule checks the independence of a contract asset"
        level @= MUST
        merge @= TERMS.TERM_014
        merge @= TERMS.TERM_016
        related @= INDEPENDENCE.IND_002
        detail @= "何をテスト、何を実装とみなすかの範囲は、範囲の決め方（REG_011 から REG_017）に定める。"

    class REG_004:
        """shikumi-contrace は、標準語彙の{{TERM_005}}が、定められた位置に置かれているかを検査する検証規則を提供しなければならない。"""

        title @= "A rule checks the positions of standard clause kinds"
        level @= MUST
        merge @= TERMS.TERM_005
        related @= CONTRACT.CTR_009

    class REG_005:
        """shikumi-contrace は、{{TERM_003}}のクラス名が、参照先のメンバー名と一致しているかを検査する検証規則を提供することが望ましい。対象型の指定とメンバーの指定を同時に持つ契約は、対象としない。"""

        title @= "A rule checks the names of member classes"
        level @= SHOULD
        merge @= TERMS.TERM_003
        related @= CONTRACT.CTR_008

    class REG_006:
        """検証規則は、診断情報を返すだけでなければならない。契約やテストの内容を書き換えたり、補正したりしてはならない。"""

        title @= "Validation reports only"
        level @= MUST_NOT

    class REG_007:
        """検証規則は、語彙が標準語彙に含まれないことを理由に診断情報を出してはならない。"""

        title @= "No validation rule rejects unknown vocabulary"
        level @= MUST_NOT
        related @= VOCAB.VOC_004

    class REG_008:
        """利用者は、自らの検証規則を追加してよい。"""

        title @= "Users may add their own validation rules"
        level @= MAY

    class REG_009:
        """診断情報の重大度は、検証規則ごとに固定しない。pytest 連携が診断情報を報告するときは、pytest の警告として報告し、重大度は利用者が決める。"""

        title @= "Severity is delegated to the user"
        level @= MUST
        related @= PYTEST_INTEGRATION.PYT_007

    class REG_010:
        """shikumi-contrace は、{{TERM_010}}を持つテストが、その条項が属する契約の{{TERM_002}}に対する{{TERM_013}}を、テスト自身、または所属するクラスに持っているかを検査する検証規則を提供することが望ましい。持っていない場合、および{{TERM_013}}の{{TERM_002}}が契約のものと一致しない場合を、診断情報として報告する。"""

        title @= (
            "A rule checks that related tests are bound to the contract's subject type"
        )
        level @= SHOULD
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_010
        merge @= TERMS.TERM_013
        detail @= "条項が属する契約は、条項のクラスを囲むクラスから辿る。契約の対象型は、契約の対象型の指定から得る。"
        related @= INDEPENDENCE.IND_007

    class REG_011:
        """{{TERM_016}}、テスト、{{TERM_014}}の範囲は、モジュールのパス（ドットで区切った接頭辞）で表す。範囲は、利用者が宣言しなければテストの宣言から導き、利用者が宣言した場合は、その宣言だけを用いる。導いた範囲と宣言した範囲の和集合は用いない。"""

        title @= "Ranges are module paths; declared ranges replace derived ones"
        level @= MUST
        merge @= TERMS.TERM_014
        merge @= TERMS.TERM_016
        detail @= "宣言があれば宣言のみ、なければ導出、とすることで、説明を単純に保ち、予想外の結果を避ける。"
        related @= INDEPENDENCE.IND_002

    class REG_012:
        """宣言がない場合、{{TERM_016}}の範囲は、{{TERM_010}}を持つテストが関係づけた条項のモジュールと、その契約が{{TERM_022}}で直接または推移的に依存する契約のモジュールから導く。テストの範囲は、{{TERM_010}}を持つテストのモジュール、{{TERM_014}}の範囲は、テストが{{TERM_013}}した{{TERM_014}}のモジュールから導く。ただし、導くときに、Python の標準ライブラリのモジュール（`builtins` を含む）は、{{TERM_014}}の範囲から除く。検査の対象は、導かれた{{TERM_016}}のモジュールとする。契約のモジュールが参照している `ports`（{{TERM_024}}）も、{{TERM_016}}の範囲に含める。"""

        title @= "Ranges are derived from the declarations in the tests"
        level @= MUST
        merge @= TERMS.TERM_010
        merge @= TERMS.TERM_013
        merge @= TERMS.TERM_014
        merge @= TERMS.TERM_016
        merge @= TERMS.TERM_022
        merge @= TERMS.TERM_024
        detail @= "導出は、テストが宣言した範囲と、その契約が依存する契約と、契約が参照する `ports` だけを対象にするため、見落としはあっても、誤検出は出ない方向になる。修飾されたモジュールパス中の `ports` は、その親パッケージの配下に参照元の契約モジュールもある場合だけ、契約資産側の境界の型として扱う。無関係な依存パッケージのモジュールパスに `ports` が含まれているだけでは、契約資産へ導出しない。トップレベルの `ports` は、配置違反を診断できるよう候補として扱う。標準ライブラリを除くのは、導出のときだけである。除かないと、実装が標準ライブラリのクラスのとき、契約が `str` を使うだけで誤検出になる。利用者が宣言した範囲は、標準ライブラリかどうかで判断しない。"
        related @= SYNTAX.SYN_015

    class REG_013:
        """導出した{{TERM_014}}の範囲は、{{TERM_014}}が定義されているモジュールだけである。再公開しているパッケージ自体など、定義されているモジュール以外への参照は、導出では検出しない。広く検査するときは、範囲を宣言する。"""

        title @= "A derived implementation range is the defining module only"
        level @= INFORMATIVE
        merge @= TERMS.TERM_014

    class REG_014:
        """shikumi-contrace は、利用者が{{TERM_016}}、テスト、{{TERM_014}}の範囲を宣言する手段を提供しなければならない。{{TERM_016}}の範囲が宣言されたときは、その配下のすべてのモジュールを検査する。"""

        title @= "Users can declare the three ranges"
        level @= MUST
        merge @= TERMS.TERM_014
        merge @= TERMS.TERM_016
        detail @= "テストから引用されない契約（孤立した契約）も、検査される。宣言の名前と書式は、公開 API の名前と配置の仕様に定める。"

    class REG_015:
        """範囲が重なるときは、最も長く一致した範囲を優先する。{{TERM_016}}の範囲が最も長く一致する参照は、許される。"""

        title @= "The longest matching range wins"
        level @= MUST
        merge @= TERMS.TERM_016
        detail @= "契約資産を、実装と同じ最上位パッケージの中に置く構成を扱うため。例えば、実装の範囲を `myproj`、契約資産の範囲を `myproj.contracts` と宣言すると、契約資産の内側の参照は許され、`myproj.service` への参照は、実装への参照として診断される。"

    class REG_016:
        """shikumi-contrace は、範囲の宣言を、{{TERM_016}}の中に置く手段を提供してはならない。"""

        title @= "Range declarations are not placed inside a contract asset"
        level @= MUST_NOT
        merge @= TERMS.TERM_016
        detail @= "契約資産の中に、テストや実装のパッケージ名を書くと、文字列であっても、契約がそれらを知っていることになり、独立性の趣旨に反する。"
        related @= INDEPENDENCE.IND_001

    class REG_017:
        """shikumi-contrace は、{{TERM_014}}の種類や配置（パッケージの構造、名前、再公開の有無）を前提にしてはならない。{{TERM_014}}の場所は、{{TERM_013}}、または利用者の宣言によってのみ知る。"""

        title @= "The layout of implementations is not assumed"
        level @= MUST_NOT
        merge @= TERMS.TERM_013
        merge @= TERMS.TERM_014
        related @= INDEPENDENCE.IND_005

    class REG_018:
        """shikumi-contrace は、Shikumi の公開 API への依存を、少数の名前に限り、内部の一か所に集約することが望ましい。"""

        title @= "Dependence on Shikumi's public API is kept small and in one place"
        level @= SHOULD
        detail @= "試作で用いた Shikumi の公開 API は、`Cardinality`、`ClassBinding`、`InformationType`、`attach_information`、`class_binding`、`information_of`、`record_descriptor_use` の七つで足りた。依存を一か所に集めることで、Shikumi の公開 API の変更や、将来の差し替えに備える。"

    class REG_019:
        """shikumi-contrace は、標準の{{TERM_019}}と標準の{{TERM_005}}の、通常は用いない組み合わせ（事後条件や不変条件に対する `violates`）を検査する検証規則を提供することが望ましい。診断情報は、警告として報告する。独自語彙は、この規則の対象としない。"""

        title @= "A rule checks unusual combinations of standard words"
        level @= SHOULD
        merge @= TERMS.TERM_005
        merge @= TERMS.TERM_019
        detail @= "対象は、標準語彙どうしの組み合わせに限る。語彙が標準に含まれないことを理由にした診断は出さない（VOC_004）。組み合わせは、標準語彙の仕様（STD_013）が、通常は用いないとするものである。"

    class REG_020:
        """shikumi-contrace は、{{TERM_022}}の宣言が契約のクラス本体に置かれ、依存先が契約であり、依存関係が循環していないことを検査する検証規則を提供しなければならない。違反は診断情報として報告する。"""

        title @= "A rule checks contract dependencies and rejects cycles"
        level @= MUST
        merge @= TERMS.TERM_022
        related @= CONTRACT.CTR_014
        related @= CONTRACT.CTR_015
        related @= SYNTAX.SYN_025
        detail @= "通常の `depends_on` は、すでに存在するクラス実体への参照だけを受け取るため、循環を作りにくい。検証は、Shikumi の低レベル API などから作られた実行時状態も含めて、循環がないことを確認する。検証は自動的な破棄や書き換えを行わない（REG_006）。"

    class REG_021:
        """shikumi-contrace は、{{TERM_023}}の宣言が{{TERM_006}}の条項に置かれていることを検査する検証規則を提供しなければならない。違反は診断情報として報告する。"""

        title @= "A rule checks the position of precondition violation behavior"
        level @= MUST
        merge @= TERMS.TERM_006
        merge @= TERMS.TERM_023
        related @= CONTRACT.CTR_016
        related @= SYNTAX.SYN_026

    class REG_022:
        """shikumi-contrace は、{{TERM_023}}を根拠として、テスト本体の構文、例外検査の有無、特定の拒否手段の有無を検査してはならない。また、`REJECTED` に関係する違反テストがないことや、`OUT_OF_SCOPE` に関係する違反テストがあることだけを理由に、診断情報を出してはならない。"""

        title @= "Validation does not infer test shape from violation behavior"
        level @= MUST_NOT
        merge @= TERMS.TERM_023
        related @= AIM.AIM_016

    class REG_023:
        """shikumi-contrace は、`ports` が契約を含んでいないこと、Protocol とデータ以外の関数やクラスを定義していないこと、および `ports` 自身の `__init__` が定義を持たないことを検査する検証規則を提供しなければならない。違反は診断情報として報告する。"""

        title @= "A rule checks that the boundary types hold only Protocols and data"
        level @= MUST
        merge @= TERMS.TERM_024
        related @= INDEPENDENCE.IND_012
        detail @= "診断コードは `ports-contract`（契約を含む）、`ports-behavior`（関数、またはデータでも Protocol でもないクラスを定義している）、`ports-definition-in-init`（`ports` の `__init__` が定義を持つ）である。データと認めるのは、dataclass、NamedTuple、TypedDict、Enum である。"

    class REG_024:
        """shikumi-contrace は、`ports` が契約または shikumi-contrace を参照していないこと、および `ports` を import する経路にある親パッケージの `__init__` が、契約または shikumi-contrace を import していないことを検査する検証規則を提供しなければならない。違反は診断情報として報告する。"""

        title @= "A rule checks that the boundary types do not drag a contract along"
        level @= MUST
        merge @= TERMS.TERM_024
        related @= INDEPENDENCE.IND_013
        detail @= "診断コードは `ports-reference`（`ports` 自身の参照）と `ports-parent`（親パッケージの `__init__` の import）である。親パッケージには、契約資産のパッケージも含む。親パッケージの検査は、`__init__` のソースの import 文を読む。テストと実装への参照は、`ports` が契約資産の範囲に入るため、既存の規則（`independence`）が検出する。"

    class REG_025:
        """範囲を宣言したときに、契約のモジュールが参照している `ports` が、宣言された{{TERM_016}}の範囲に入っていない場合、shikumi-contrace は、診断情報として報告しなければならない。"""

        title @= "A declared range that leaves out the boundary types is reported"
        level @= MUST
        merge @= TERMS.TERM_016
        merge @= TERMS.TERM_024
        related @= INDEPENDENCE.IND_010
        detail @= "宣言した範囲は、導出した範囲を置き換える（REG_011）ので、`ports` を自動では含めない。含め忘れると、`ports` が検査から漏れる。どの `ports` を契約資産側の境界の型とみなすかは REG_012 と同じであり、無関係な依存パッケージの `ports` は対象にしない。診断コードは `ports-undeclared` である。"

    class REG_026:
        """shikumi-contrace は、契約のモジュールが、どの契約の{{TERM_002}}でもない Protocol を定義していないことを検査する検証規則を提供しなければならない。違反は診断情報として報告する。"""

        title @= "A rule checks that value shapes are not defined in contract modules"
        level @= MUST
        merge @= TERMS.TERM_002
        merge @= TERMS.TERM_024
        related @= INDEPENDENCE.IND_011
        detail @= "診断コードは `shape-outside-ports` である。モジュールの直下に定義された Protocol だけを対象とする。dataclass などのデータの型は、対象としない。"

    class REG_027:
        """shikumi-contrace は、`ports` を直下に持つパッケージの構造、すなわち `ports` がパッケージであり、その直下がモジュールだけであることを、Shikumi の構造の規定として表し、その適合を検査しなければならない。構造の規定は、`CONTRACT_ASSET_STRUCTURE` として公開する。違反は診断情報として報告する。"""

        title @= (
            "The structure of the contract asset is a Shikumi structure specification"
        )
        level @= MUST
        merge @= TERMS.TERM_016
        merge @= TERMS.TERM_024
        related @= INDEPENDENCE.IND_010
        detail @= "Shikumi の構造の規定は、ルートからの相対で書かれ、ルート自身の名前を持たない。そのため、契約資産のパッケージの名前は任意であり、固定の名前は `ports` だけである。ルート直下の他の子は、名前が任意のモジュールまたはサブパッケージである。`ports` は必須にしない。契約が値の形を持たなければ、`ports` は要らないためである。構造の規定が扱うのはトポロジーだけなので、モジュールの中身（定義の種類、参照）は対象外である（IND_012、IND_013）。診断コードは `ports-structure` で、Shikumi の構造の診断のメッセージを含む。公開した規定は、Shikumi 自身の検証（`validate` の `structure_specification`）に、そのまま渡せる。"

    class REG_028:
        """shikumi-contrace は、`ports` を直下に持つパッケージが、テストまたは実装を含んでいる場合、および `ports` がパッケージの外にある（トップレベルにある）場合を、診断情報として報告しなければならない。"""

        title @= "A rule checks that ports is placed directly inside a contract asset"
        level @= MUST
        merge @= TERMS.TERM_016
        merge @= TERMS.TERM_024
        related @= INDEPENDENCE.IND_015
        detail @= "診断コードは `ports-placement` である。テストと実装の範囲は、宣言されたもの、または導出されたものを使う。導出は、テストが宣言した範囲だけを使うので、束縛されていない実装は見落とす。見落とす方向であり、誤検出にはならない。"
