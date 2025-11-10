# AGENTS.md

このファイルは、LLM/AIエージェントがリポジトリを扱う際の最小限のガイダンスです。

## 原則
- ユーザーとは**日本語**で会話すること。
- **Serenaを積極活用すること。**(projectは"clover_announcement_bot"とする)(使用可能な場合) 
- **Context7を利用すること。**(使用可能な場合)
- **入念に現状実装やドキュメントを参照、分析してから実装を行うこと。**
- ユーザーからの指示がない限り、**python scriptによるコード解析やワンライナー実行は禁止**。
- **`git rm`や`rm`などのファイル削除は禁止**（ユーザーに提案し、実行は待つ）
- **[@docs/standards/documentation_guidelines.md](docs/standards/documentation_guidelines.md)と[@docs/standards/documentation_operations.md](docs/standards/documentation_operations.md)に従い、積極的にドキュメント運用・記述を行う**
- 日付確認には`date`コマンドを使用すること


## 開発ルール
- **Git**:  
  - コミットメッセージは英語、形式例: `feat: add analytics screen`  
  - ブランチ: `feature/`, `fix/`, `chore/`（ベースは`dev`）  
  - PRタイトルも同形式、説明に目的・影響を記載  

- **ドキュメンテーション**:
  - ドキュメントを基軸として開発・運用を行う
  - **すべての新機能・変更は関連ドキュメントを更新すること**
  - draft | survey -> plan -> intent -> (guide | reference) の流れを遵守すること