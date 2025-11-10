---
title: "メッセージ送信モーダル リファレンス"
domain: "bot"
status: "beta"
version: "0.1.0"
created: "2025-11-09"
updated: "2025-11-09"
related_plan: "docs/plan/bot/messaging-modal-port/plan.md"
related_intents:
  - "docs/intent/bot/messaging-modal-port/intent.md"
---

## モジュール構成
| モジュール | 役割 |
| --- | --- |
| `src/app/config.py` | `.env` から `DISCORD_BOT_TOKEN` を読み込み `AppConfig` を返す |
| `src/app/container.py` | `BotClient` を生成し `/setup` コマンドを登録して `DiscordApplication` を返す |
| `src/bot/client.py` | `discord.Client` 拡張。`CommandTree` を保持し `on_ready` で `tree.sync()` を実行 |
| `src/bot/commands.py` | `/setup` Slash コマンドを登録し、View を含むフォローアップを送信 |
| `src/views/view.py` | `SendModalView` と `SendMessageModal` を定義し、入力値検証を `process_modal_submission` に集約 |
| `src/main.py` | `load_config` → `build_discord_app` → `DiscordApplication.run()` を結線するエントリポイント |

## Slash コマンド `/setup`
- `name`: `setup`
- `description`: `メッセージ送信のセットアップを行います。`
- 応答フロー:
  1. `interaction.response.defer(ephemeral=True)` で応答ウィンドウを確保。
  2. `interaction.followup.send(..., view=SendModalView(), ephemeral=True)` で View を返す。

## SendMessageModal
- TextInput
  - `channel_id`: 必須, 数値 ID
  - `message`: 必須, Paragraph
- エラーメッセージ

| キー | 内容 |
| --- | --- |
| `ERROR_INVALID_ID` | `チャンネルIDは有効な整数である必要があります。` |
| `ERROR_CHANNEL_NOT_FOUND` | `チャンネルが見つかりません...` |
| `ERROR_GENERAL` | `エラー: {error}` |
| `SUCCESS_MESSAGE` | `<#{channel_id}> にメッセージを送信しました。` |

- `process_modal_submission` のロジック
  1. `channel_id_value` を `int()` 変換できなければ即終了。
  2. `interaction.client.get_channel()` → 無ければ `fetch_channel()` を順に試行。
  3. `discord.NotFound` は `ERROR_CHANNEL_NOT_FOUND`、`discord.HTTPException` は `ERROR_GENERAL` で通知。
  4. `Messageable` でないチャンネルは拒否。
  5. `channel.send(message_value)` を await 後、成功メッセージを ephemeral で返す。

## 設定
- `.env`
  - `DISCORD_BOT_TOKEN`: Discord Bot のトークン (必須)。
- `.env` が存在しない場合は `python-dotenv` が例外を投げるため、README 手順で必ず作成する。

## 実行スクリプト
- `poetry run clover-announcement-bot`
  - `src/main.py` の `main()` を呼び出し、ログレベル `INFO` で起動する。
- 代替: `poetry run python -m src.main`

## テストカバレッジ
- `tests/views/test_send_message_modal.py`: 入力検証とエラー分岐。
- `tests/bot/test_commands.py`: Slash コマンド登録と View 返却の検証。
