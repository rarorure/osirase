---
title: "ds_rin_bot メッセージ送信モーダル移植計画"
domain: "bot"
status: "draft"
version: "0.1.0"
created: "2025-11-09"
updated: "2025-11-09"
related_issues: []
related_prs: []
references:
  - "ds_rin_bot/src/views/view.py#L11-L80"
  - "ds_rin_bot/src/bot/commands.py#L24-L37"
  - "ds_rin_bot/src/app/container.py#L23-L74"
  - "ds_rin_bot/src/app/config.py#L14-L118"
  - "ds_rin_bot/src/main.py#L12-L34"
scope:
  - "discord.py 2.6 系を用いたクライアント初期化・コマンド登録の最小構成を clover_announcement_bot に導入する"
  - "ds_rin_bot のメッセージ送信モーダル UI と /setup コマンドの体験を同等レベルで再現する"
  - "環境変数ベースのトークン読み込みとエラー通知のロギング基盤を整備する"
non_goals:
  - "ds_rin_bot の一時 VC やチャンネルブリッジといった周辺機能の移植"
  - "複数ギルド間の連携や TinyDB 依存機構の導入"
requirements:
  - "Python 3.12 + discord.py 2.6 系で動作すること"
  - "DISCORD_BOT_TOKEN を .env / 環境変数から安全に読み込むこと"
  - "セットアップメッセージからボタン経由でモーダルを開ける UX を保証すること"
constraints:
  - "現在のリポジトリにはアプリケーションコードが存在しないため、新規に src/ 構造を定義する必要がある"
  - "ユーザー操作文言は ds_rin_bot と同等の日本語表現を維持する"
api_changes:
  - "新規 Slash Command `/setup` を追加し、フォローアップメッセージと View を送信する"
data_models:
  - "ストレージ不要。UI 状態のみ (discord.ui.View/Modal) を扱う"
migrations:
  - "データ移行は不要。環境変数 (.env.example) を新規追加するのみ"
rollout_plan:
  - "ステージングサーバーで新 Bot を起動し、/setup→モーダル送信の動作確認後に本番トークンへ切り替える"
  - "初回デプロイは GitHub Actions ではなく手動起動で行い、ログを監視する"
rollback:
  - "環境変数から Bot トークンを抜く / サービス停止で即時ロールバック"
  - "Poetry 依存追加のみなので revert で元の空リポジトリ状態に戻せる"
test_plan:
  - "view/modal の単体テスト: channel ID パース、エラーハンドリングの単体テスト (discord.py のモック使用)"
  - "アプリ起動・コマンド登録の結合テスト: discord.app_commands.CommandTree をモックし register_commands が呼ばれることを検証"
  - "手動テスト: Discord サーバーで /setup → モーダル送信 → 対象チャンネル投稿確認"
observability:
  - "logging.basicConfig(level=INFO) で最低限のログ出力を行い、モーダル送信失敗時は LOGGER.exception を使用する"
security_privacy:
  - "DISCORD_BOT_TOKEN を .env で管理し、リポジトリにはコミットしない"
  - "モーダルで送信されたメッセージ内容はログに残さない"
performance_budget:
  - "Slash コマンド1件・メッセージ送信のみで負荷は軽微。API レート制限を超えないことを確認する"
i18n_a11y:
  - "UI テキストは現状どおり日本語で統一し、ボタン/モーダルのラベルは 20 文字以内を維持する"
  - "エラーメッセージはすべて ephemeral メッセージで返し、コマンド利用者以外に見えないようにする"
acceptance_criteria:
  - "clover_announcement_bot で `/setup` が成功し、モーダルを開ける"
  - "有効なチャンネル ID で送信すると対象チャンネルへメッセージが投稿され、成功通知が ephemeral で返る"
  - "無効な ID・アクセス不可チャンネル・例外発生時に ds_rin_bot 同等のエラーメッセージが表示される"
owners:
  - "clover announcement bot maintainers"
---

## 背景と目的

- `ds_rin_bot` では `/setup` コマンドから `SendModalView` を掲出し、任意のチャンネルへテキスト送信できるモーダルを提供している（`src/views/view.py#L11-L80`, `src/bot/commands.py#L24-L37`）。  
- `clover_announcement_bot` はまだ Discord クライアントやコマンド登録の実装が存在せず、告知メッセージを柔軟に送信するための UI が欠落している。  
- 本計画は、メッセージ送信機能を最小の基盤ごと移植し、後続の機能追加に再利用できる構造を整備することを目的とする。

## 既存実装の要点 (ds_rin_bot)

| 要素 | 内容 |
| --- | --- |
| UI 層 | `SendModalView` と `SendMessageModal` がボタン-モーダル連携を担当し、チャンネル解決と送信処理を内包する。 |
| コマンド層 | `register_commands` が `/setup` コマンドを生やし、フォローアップメッセージへ `SendModalView` を添付する。 |
| アプリ基盤 | `BotClient` と `build_discord_app` が Intents, CommandTree, ロギング、依存管理を担い、`main.py` で `asyncio.run` エントリポイントを提供する。 |
| 設定 | `load_config` が `.env` から `DISCORD_BOT_TOKEN` を読み、DiscordApplication に注入する。 |

これらは互いに疎結合であり、メッセージ送信モーダルだけであれば Temp VC や Bridge のモジュールに依存しない。

## ターゲットアーキテクチャ (clover_announcement_bot)

1. **アプリ階層**
   - `src/app/config.py`: `.env` からトークンを読む最小構成 (`DiscordSettings`, `AppConfig`, `load_config`)。
   - `src/app/container.py`: `DiscordApplication` と `build_discord_app` を定義し、`BotClient` を組み立てて `register_commands` を実行。
2. **Bot 階層**
   - `src/bot/client.py`: `discord.Client` を継承し `tree.sync()` を `on_ready` で実施。
   - `src/bot/commands.py`: `/setup` のみを登録し、`SendModalView` を利用。
3. **View 階層**
   - `src/views/view.py`: `SendModalView`, `SendMessageModal` と関連テキストをそのまま移植。`Messageable` 判定と例外ハンドリングも踏襲。
4. **Entrypoint**
   - `src/main.py`: `load_config`→`build_discord_app`→`DiscordApplication.run()` のフローを実装し、Poetry スクリプトから起動可能にする。
5. **ドキュメント & Ops**
   - `README.md` に動かし方、`.env.example` に必要変数を記述。
   - `docs/guide/` / `docs/reference/` への追記は実装後に実施（本 Plan では対象外だが、intent/guide 更新のトリガーとなる）。

## 実装ステップ

### フェーズ1: 基盤整備
1. `pyproject.toml` に `python-dotenv` を追加し、開発環境で `poetry install` を行う。
2. `src/` ディレクトリと `__init__.py` を整備し、`app`, `bot`, `views` パッケージを構築する。
3. `.env.example` を追加して `DISCORD_BOT_TOKEN` のみ定義。README にセットアップ手順を追記。

### フェーズ2: Discord クライアントと UI の移植
1. `bot/client.py` へ `BotClient` を実装し、`tree.sync()`・ログ出力など ds_rin_bot と同じ責務を持たせる。
2. `views/view.py` に `SendModalView` と `SendMessageModal` を移植。Discord API 呼び出し部分は `ds_rin_bot/src/views/view.py#L11-L80` を参照しながら typing とロギングを整える。
3. `bot/commands.py` に `/setup` コマンドのみを実装し、View を添付したフォローアップメッセージを送信する。
4. `app/container.py` で `BotClient` を生成し `register_commands` を await、`DiscordApplication` から `client.start(token)` を呼び出せるようにする。
5. `app/config.py` と `main.py` を ds_rin_bot 相当で作成し、エラー時のログ・例外取扱いを踏襲する。

### フェーズ3: 動作確認と仕上げ
1. 単体テスト: Modal の `on_submit` を pytest + `pytest-asyncio` で検証（成功/失敗パターン、ephemeral 応答）。
2. 起動テスト: `poetry run python -m src.main` でローカル起動し、Discord テストサーバーで `/setup` を実行。
3. ドキュメント更新: README に起動手順、docs/guide へ利用ガイド、docs/reference へ API 仕様（別PR可）を準備。
4. intent 作成トリガー: 本 plan を根拠に `docs/intent/bot/messaging-modal-port/intent.md` を後続で作成し、承認後に必要なら archives へ移動。

## リスクと対応

| リスク | 影響 | 対応策 |
| --- | --- | --- |
| Discord API バージョン差異 | Slash コマンド登録が失敗する | ds_rin_bot と同じ discord.py バージョン (2.6 系) を採用し、`tree.sync()` のログを必ず確認する。 |
| 起動構成の不足 | `.env` 未設定でクラッシュ | `load_config` で ValueError を投げ、README/.env.example で必須変数を明記する。 |
| 依存不足による lint/test 失敗 | CI で停止 | Poetry.lock を再生成し、pip install 用に明示的な依存を追加する。 |

## ロールアウト後のフォローアップ

- `/setup` の利用ログを監視し、エラー頻度を可観測化（ログ出力を CloudWatch 等に連携予定）。
- 告知テンプレート機能や複数メッセージ送信機能を追加する際は、本計画の構成を再利用し、intent ドキュメントで意図を整理する。

