---
title: "メッセージ送信モーダル運用ガイド"
domain: "bot"
status: "active"
version: "0.1.0"
created: "2025-11-09"
updated: "2025-11-09"
related_intents:
  - "docs/intent/bot/messaging-modal-port/intent.md"
references:
  - "docs/reference/bot/messaging-modal-port/reference.md"
---

## 概要
- `/setup` Slash コマンドからメッセージ送信用モーダルを開き、任意チャンネルへ告知文を投稿する機能。
- 送信成功/失敗はすべて ephemeral メッセージで発報する。

## 事前準備
1. `DISCORD_BOT_TOKEN` を `.env` で定義し、Bot を Discord サーバーに参加させる。
2. Bot に対象チャンネルへの送信権限 (Send Messages) を付与しておく。
3. `poetry run clover-announcement-bot` で起動し、ログに `準備完了` が出力されていることを確認する。

## 利用手順
1. Discord サーバーで `/setup` を実行する。
2. フォローアップメッセージの「メッセージ送信」ボタンを押す。
3. モーダルに以下を入力し「送信」を押下する。
   - **チャンネルID**: 送信先の数値 ID。右クリック→IDをコピー で取得。
   - **本文**: Discord に投稿したいテキスト (改行可)。
4. 成功時: `<#channel_id>` へ投稿され、利用者にのみ成功メッセージが表示される。
5. 失敗時: エラーごとの説明 (無効 ID / 権限不足 / 例外) が ephemeral で返る。

## トラブルシューティング
| 症状 | 原因 | 対応 |
| --- | --- | --- |
| `チャンネルIDは有効な整数である必要があります。` | ID 入力が数値でない | Discord の開発者モードから ID をコピーし直す |
| `チャンネルが見つかりません...` | Bot がギルド/チャンネルを参照できない | Bot を対象サーバーに追加し、対象チャンネルで送信権限を付与 |
| `エラー: ...` | Discord API / ネットワーク例外 | ログ (`LOGGER.exception`) を確認し、再試行 or 権限/レート制限を調査 |

## 運用 Tips
- Slash コマンド実行者以外にはフォローアップ/エラー文は見えないため、権限付きアナウンス担当者のみを想定して運用できる。
- 複数メッセージを連続で送る場合は `/setup` を再実行して新しい View を取得する。
- Bot の稼働確認は `/setup` 実行で View が返るかどうかが最も手軽。
