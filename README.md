# clover_announcement_bot

Discord 上で告知メッセージを安全に配信するための最小限の Slash コマンド `/setup` とメッセージ送信モーダルを提供します。

## セットアップ
1. 依存関係をインストールします。
   ```bash
   poetry install
   ```
2. `.env.example` をコピーして Discord Bot トークンを設定します。
   ```bash
   cp .env.example .env
   # DISCORD_BOT_TOKEN=xxx を入力
   ```
3. Bot を起動します。
   ```bash
   poetry run clover-announcement-bot
   # もしくは
   poetry run python -m src.main
   ```

## Slash コマンド `/setup`
- `/setup` を実行すると、フォローアップで「メッセージ送信」ボタン付きの View が返り、モーダルから任意チャンネルへ本文を投稿できます。
- 正常に送信できた場合は `<#channel_id>` への送信結果を ephemeral メッセージで通知します。
- 無効なチャンネル ID や権限不足時はエラーメッセージを ephemeral で返します。

## テスト
- モーダルの検証ロジックと Slash コマンド登録を `pytest` + `pytest-asyncio` でカバーしています。
- 実行例:
  ```bash
  poetry run pytest
  ```

## ドキュメント
- 計画: `docs/plan/bot/messaging-modal-port/plan.md`
- Intent: `docs/intent/bot/messaging-modal-port/intent.md`
- 利用ガイド: `docs/guide/bot/messaging-modal-port/guide.md`
- リファレンス: `docs/reference/bot/messaging-modal-port/reference.md`
