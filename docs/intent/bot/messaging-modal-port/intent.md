---
title: "メッセージ送信モーダル移植 Intent"
domain: "bot"
status: "active"
version: "0.1.0"
created: "2025-11-09"
updated: "2025-11-09"
related_plan: "docs/plan/bot/messaging-modal-port/plan.md"
owners:
  - "clover announcement bot maintainers"
---

## 背景
- `ds_rin_bot` に実装済みの `/setup` + モーダル UI を clover 側にも導入し、告知メッセージを柔軟に送れるようにする必要があった。
- 当リポジトリにはアプリケーションコードが存在しなかったため、`src/` 階層と設定読み込み〜エントリポイントを一式整備する必要があった。

## 決定事項
1. **アーキテクチャ**: `app/config.py` `app/container.py` `bot/` `views/` `main.py` を `ds_rin_bot` と同じ責務分割で新設する。
2. **UI**: `SendModalView` / `SendMessageModal` を移植し、Messageable 判定と例外処理を踏襲。入力値検証は関数 (`process_modal_submission`) へ切り出し、単体テストしやすくした。
3. **コマンド**: `/setup` のみを `register_commands` で登録し、フォローアップを ephemeral 応答で返す。
4. **設定**: `.env` から `DISCORD_BOT_TOKEN` を読み込む `load_config` を実装し、スクリプトエントリを `pyproject` の `scripts` に追加。
5. **テスト/依存**: `pytest` `pytest-asyncio` `python-dotenv` を導入し、モーダル処理と Slash コマンド登録を単体テスト。

## トレードオフと理由
- エントリポイントは `discord.Intents.all()` を用い、将来的な機能追加時の意図せぬ不足を避けた (必要に応じて絞り込む)。
- モーダルの入力チェックを外部関数化し、UI コールバック自体へのユニットテストは諦める代わりにロジックの再利用性を確保。
- 初期デプロイでは TinyDB 等のストレージを持たず、後続の追加機能で必要になったタイミングで導入する。

## 影響範囲
- 新規に `src/` 階層を追加し、既存依存には影響しない。
- `.env.example` を追加し、README/guide/reference を起点に運用手順を共有。

## テスト&観測方針
- `pytest` ベースで Modal/Slash コマンドをモック検証し、CI での自動実行を想定。
- runtime 中は `logging.basicConfig(level=INFO)` でエラー通知を記録し、モーダル送信失敗時は `LOGGER.exception` を発火する。

## フォローアップ
1. Discord Bot 実行ユーザー/サーバーで `/setup` を試験し、ログ&権限を確認。
2. 告知テンプレート機能など次段の intent/draft を立ち上げる際は本構造を基盤として再利用する。
