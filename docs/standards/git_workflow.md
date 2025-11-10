# clover_announcement_bot Git 運用基準

## 目的
- コミット、ブランチ、プルリクエスト運用を統一し、履歴とレビュー品質を維持する。
- 開発者間で一貫した Git 運用を実現する。

## コミットメッセージ
- 先頭にカテゴリを付与する: `feat:` `fix:` `refactor:` `style:` `perf:` `docs:` `build:` `ci:` `test:` `chore:`
- 英語で簡潔に記述し、感情的・主観的な表現は避ける。
- 1 行目に要約を記載し、必要に応じて 3〜5 行ほどの詳細を箇条書きで追記する。

### 例
```
feat: add analytics presentation layer

- Add analytics screens for main view, inventory, and sales analytics
- Implement analytics UI widgets including charts and stats cards
- Add index file for organized widget exports
```

## ブランチ戦略
- 新規ブランチ名は用途に応じて `feature/` `fix/` `chore/` を接頭辞として用いる。
- 通常は `dev` ブランチをベースに作業ブランチを作成する。

## プルリクエスト
- タイトルはコミット要約と同様の形式で記載する。
- 説明には変更内容の概要・目的・影響範囲を明記する。
- レビュー担当者が判断しやすいよう、関連ドキュメントやテスト結果を併記する。

# prefixについて
- `feat:` 新機能追加
- `fix:` バグ修正
- `refactor:` リファクタリング
- `style:` コードフォーマット・スタイル修正（動作に影響しない変更）
- `perf:` パフォーマンス改善
- `docs:` ドキュメント修正・追加
- `build:` ビルド関連の変更
- `ci:` CI/CD 設定の変更
- `test:` テストコードの追加・修正
- `chore:` その他雑務的な変更