"""shikumi-contrace の Project Status の正本ソース。"""

from shikumi_devdoc.fields.status import GENERAL, condition, kind
from shikumi_devdoc.norms.common import canonical_source
from shikumi_devdoc.norms.document import title


@canonical_source(
    "{{project.name}} Project Status",
    filename="STATUS.md",
    merge_policy="external",
    heading="identity",
)
class PROJECT_STATUS:
    r"""
    `{{project.name}}` の現在状態と、現在から見た将来の告知を記述する。
    過去の状態変化は保持せず、実際に起きた利用者向け変更は CHANGELOG が担当する。
    仕様書には決まったことだけを書き、決まっていないことは、この文書の告知（`NOTICE_NNN`）に記録する。
    """

    class STATUS_001:
        r"""
        最初の公開版 `0.1.0` をリリースした。本体、読み取り API、検証 API、任意の pytest 連携を実装し、テストは Python 3.11 と 3.12 で通っている。型の検査は、basedpyright と mypy で確認している。英語の公開文書を公開している。
        """

        title @= "Development stage"

    class STATUS_002:
        r"""
        対象の Python バージョン範囲は `{{project.requires-python}}` とする予定である。基盤とする Shikumi が 3.11 以上を必要とすることによる。
        """

        title @= "Supported Python"

    class STATUS_003:
        r"""
        `{{project.name}}` の設計は、仕様書（`docs/specification/`）に記述している。仕様書が実装の基準であり、実装は仕様書の記述に従って行う。仕様書と実装が食い違う場合は、実装ではなく仕様書の記述を先に見直す。
        """

        title @= "Design and implementation"

    class STATUS_004:
        r"""
        `{{project.name}}` は、旧 `speclike`（PyPI に公開されている 0.0.x）とは設計思想が異なるため、別の名前の新しいプロジェクトとして始めた。`speclike` の公開名や機能、変更履歴は、引き継がない。
        """

        title @= "Relationship to speclike"

    class STATUS_005:
        r"""
        文書は `shikumi-devdoc` で管理する。正本ソースは `devdocs/canonical_sources/`、そこから生成した日本語の正本は `devdocs/canonical_documents/` にある。英語の公開文書（`README.md`、`STATUS.md`、`CHANGELOG.md`、`docs/`）は、日本語の正本を翻訳したものであり、正本と同じ構造を保つ。
        """

        title @= "Documentation system"

    class STATUS_006:
        r"""
        基盤とする Shikumi は、現在の版（0.2.4）以上を要件とし、上限は設けない。Shikumi は 0.2 系であり、公開 API が変わる可能性があるが、Shikumi と `{{project.name}}` の間で調整する。
        """

        title @= "Shikumi version requirement"

    class STATUS_007:
        r"""
        `{{project.name}}` は、metamk の現在の版（0.1.0）以上に依存し、`metamk.Mk` を `Phase` という名前で、`phase_of` を同名で再エクスポートする。上限は設けない。`Phase` の振る舞いは `metamk.Mk` に従う。
        """

        title @= "metamk requirement and re-export"

    class STATUS_008:
        r"""
        リポジトリは `minoru-jp/shikumi-contrace` を新設し、旧 `speclike` は、README に `shikumi-contrace` への案内を足して、アーカイブする予定である。ライセンスは MIT とする。
        """

        title @= "Repository and license"

    class NOTICE_014:
        r"""
        新しい設計の最初の公開版から 1.0 までの間は、公開 API を予告なく変更することがある。
        """

        title @= "API stability before 1.0"
        kind @= GENERAL
        condition @= "最初のメジャーバージョンを公開するまで。"
