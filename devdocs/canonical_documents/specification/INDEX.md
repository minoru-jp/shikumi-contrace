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

# shikumi-contrace 仕様書

| Document | Summary |
| --- | --- |
| [目的と範囲](aim.md) | shikumi-contrace の目的と、範囲外とすること。 |
| [契約の構造](contract.md) | 契約を構成する実体（対象型、メンバー、条項）と、その位置の規則。 |
| [契約の独立性](independence.md) | 契約を、テストにも実装にも依存しない独立した資産として保つための規則と、依存の向き。 |
| [テスト側の記述](test_side.md) | テストを契約の条項に関係づける記述、注釈、束縛。 |
| [記述器と書式](syntax.md) | 契約とテストの側で使う記述器の名前と、その書式。束縛の書式を含む。 |
| [情報の読み取り](reading.md) | 宣言された契約とテストの情報を読み取る、テストランナーに依存しない API。条項とテストの対応の追跡。 |
| [公開 API の名前と配置](api.md) | 公開 API を置く場所と、読み取り・検証・pytest 連携の API の名前。 |
| [語彙](vocab.md) | 標準語彙の提供と、独自語彙を妨げないこと、未知の語彙を拒否しないこと。 |
| [標準語彙](standard_vocabulary.md) | 標準の条項種別、違反時の扱い、関係語、注釈語と、その意味。 |
| [規定体と検証](regulation.md) | 契約の構造と独立性を検査する検証規則、参照を制限する範囲の決め方、検査の性質および限界。 |
| [pytest 連携（任意）](pytest_integration.md) | pytest 連携を任意の連携として提供するときに守ること。本体との分離、診断の出し方、情報の持ち方、提供する機能の範囲。 |
