"""shikumi-contrace の CHANGELOG の正本ソース。"""

from shikumi_devdoc.fields.changelog import (
    added,
    released_on,
    version,
)
from shikumi_devdoc.norms.common import canonical_source


@canonical_source(
    "shikumi-contrace 変更履歴",
    filename="CHANGELOG.md",
    merge_policy="forbidden",
    heading="identity",
)
class CHANGELOG:
    """`shikumi-contrace` の版ごとの変更履歴を記録する。`shikumi-contrace` は `speclike` とは別の新しいプロジェクトであり、`speclike` の変更履歴は引き継がない。"""

    class V0_1_0:
        """最初の公開版。"""

        version @= "0.1.0"
        released_on @= "2026-10-07"

        added @= "契約を記述する記述器 `subject`、`member`、`kind` と、標準の条項種別 `PRE`、`POST`、`INV` を追加した。"
        added @= "テストを条項に関係づける関係語 `upholds`、`violates` と、17 の標準の注釈語を追加した。注釈語は、クラス本体の `@=` と、デコレータの両方で書ける。"
        added @= "契約の対象型と実装を結ぶ束縛 `binds[Subject](Impl)` を追加した。型チェッカーが、実装の適合を検査できる。対象型は、型引数を与えた総称型（`Inventory[Reservation]`）でもよい。"
        added @= "独自語彙の生成器 `define` を追加した。"
        added @= "metamk の `Mk` を `Phase` という名前で、`phase_of` を同名で再エクスポートした。"
        added @= "読み取り API `shikumi_contrace.reading` を追加した。`untested_clauses` は、記録された関係づけを持つテストのない条項を一覧する。"
        added @= "契約同士の一方向の依存を記述する `depends_on` と、依存を正引き・逆引きする `dependencies_of`、`dependents_of` を追加した。依存の誤配置、契約でない対象への依存、循環依存を検証する。"
        added @= "契約と実装が共有する値の形（境界の型）を、契約資産のパッケージの直下の `ports` パッケージに置く規定と、その検査を追加した。構造（`ports` がパッケージで、直下がモジュールだけ）は、Shikumi の構造の規定 `CONTRACT_ASSET_STRUCTURE` で検査する。そのほか、`ports` が契約や関数を含むこと、`ports` の `__init__` が定義を持つこと、契約や `shikumi-contrace` を参照すること、親パッケージの `__init__` がそれらを import すること、`ports` を含むパッケージがテストや実装を含むこと、範囲の宣言から `ports` が漏れること、契約の module が対象型でない Protocol を定義することを検証する。"
        added @= "事前条件の違反時の扱いを記述する `on_violation` と、標準値 `OUT_OF_SCOPE`、`REJECTED` を追加した。違反時の実装方法やテスト本体の形は推論・強制しない。"
        added @= "検証 API `shikumi_contrace.checking` を追加した。契約資産の独立性、条項の位置、メンバーの名前、束縛、標準語彙の通常は用いない組み合わせを検査する。"
        added @= "任意の pytest 連携 `shikumi_contrace.pytest` を追加した。失敗したテストの出力への契約情報の表示と、選んだときだけの収集時の検証を提供する。"
