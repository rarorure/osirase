# Documentation Guide

> **必読:** ドキュメントのアーカイブ運用・承認フローに関する最新ルールは、常に `docs/standards/documentation_operations.md` を参照し
> て遵守してください。

## このガイドの位置づけ
- プロジェクト内でドキュメントを作成・更新する際の入口となる案内板です。
- 迷ったときは、まず本ファイルから関連ドキュメントを辿り、必須ポリシーを確認してください。
- 詳細な執筆・レビュー手順は `docs/standards/documentation_guidelines.md`、アーカイブ運用や承認プロセスは `docs/standards/documentati
on_operations.md` を必ず確認します。

## 参照すべき中核ドキュメント
1. **`docs/standards/documentation_operations.md`**
   - 一時ドキュメント (`draft`/`plan`/`survey`) から `intent` への移行、`docs/archives/` へのアーカイブ手順、違反時の対処までを規定し
   ています。
   - `intent` 承認前のアーカイブ禁止など、レビュープロセスで必須となるルールが整理されています。
2. **`docs/standards/documentation_guidelines.md`**
   - ドキュメント体系、各ディレクトリの役割、front-matter の必須項目をまとめた実務ガイドラインです。
   - 執筆時のテンプレートやレビュー観点を確認する際に参照してください。
3. **`docs/plan/docs/documentation-operations-policy/plan.md`**
   - ドキュメント運用刷新に関する中長期的な計画書です。
   - 標準やガイドラインの改訂背景、段階的な自動化ロードマップを確認できます。

## 利用者へのお願い
- 新しいドキュメントを追加するときは、上記 3 文書を読み、運用・レビューの前提条件に矛盾がないかを確認してください。
- `intent` 承認後にアーカイブを行う場合は、PR の説明欄で対象ドキュメントと移行先を明示し、レビュワーにも周知してください。
- ガイドラインに改善点を見つけた場合は、`docs/draft/` で議論を開始し、合意形成後に標準ドキュメントを更新してください。

## 最終更新の扱い
- 本ファイルを更新した場合は、`docs/standards/documentation_operations.md` と `docs/standards/documentation_guidelines.md` の整合性
  を確認してください。

## Front-matter クイックリファレンス

ドキュメントを作成・更新する際に必要な front-matter フィールドを素早く確認できるよう、本セクションにまとめました。
詳細な定義や背景については、`docs/standards/documentation_operations.md` の「Front-matter Schema」セクションを参照してください。

### ドキュメント種別別フィールド一覧

| フィールド | draft | plan | intent | survey | guide / reference | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| `title` | ✓ | ✓ | ✓ | ✓ | ✓ | ドキュメント名（英語、シンプルに） |
| `domain` | ✓ | ✓ | ✓ | ✓ | ✓ | 所属ドメイン例：`security`, `auth`, `payments`, `docs` |
| `status` | ✓ | ✓ | ✓ | ✓ | ✓ | 状態：`proposed`, `active`, `deprecated`, `superseded` |
| `version` | ✓ | ✓ | ✓ | ✓ | ✓ | セマンティック or 整数。更新のたび +1 |
| `created` / `updated` | ✓ | ✓ | ✓ | ✓ | ✓ | `YYYY-MM-DD` 形式。`updated` は更新時に必ず変更 |
| `related_issues` / `related_prs` | ✓ | ✓ | ✓ | ✓ | ✓ | GitHub 番号配列（例：`[#123, #456]`） |
| `references` | ✓ | ✓ | ✓ | ✓ | ✓ | 関連ドキュメントへの相対リンク |
| **draft 専用フィールド** | | | | | | |
| `state` | ✓ | - | - | - | - | 検討段階：`idea`, `exploring`, `paused` |
| `hypothesis` | ✓ | - | - | - | - | 検証したい仮説（リスト形式可） |
| `options` | ✓ | - | - | - | - | 代替案や選択肢（比較表可） |
| `open_questions` | ✓ | - | - | - | - | 未解決事項のリスト |
| `next_action_by` | ✓ | - | - | - | - | 次アクション担当者 |
| `review_due` | ✓ | - | - | - | - | 見直し期限（`YYYY-MM-DD`） |
| `ttl_days` | ✓ | - | - | - | - | 自動失効までの日数（既定 30） |
| **plan 専用フィールド** | | | | | | |
| `scope` / `non_goals` | - | ✓ | - | - | - | 対象範囲と対象外を明文化 |
| `acceptance_criteria` | - | ✓ | - | - | - | 完了条件（測定可能であること） |
| `rollout_plan` / `rollback` | - | ✓ | - | - | - | リリース段階と失敗時対応 |
| `test_plan` / `observability` | - | ✓ | - | - | - | テスト戦略とログ・メトリクス方針 |
| `security_privacy` | - | ✓ | - | - | - | 機密情報・個人情報の取扱方針 |
| `supersedes` / `superseded_by` | - | ✓ | - | - | - | 旧/新 plan との関係（任意） |

### よくある更新パターン

#### 1. draft を作成する
```yaml
status: proposed          # 常に proposed で開始
state: idea               # 初期値は idea
ttl_days: 30              # 既定値
created: YYYY-MM-DD       # 今日の日付
updated: YYYY-MM-DD       # 今日の日付
```

#### 2. draft で検討を進める
```yaml
state: exploring          # 検討進行中に変更
hypothesis: [...]         # 仮説を追記・更新
open_questions: [...]     # 未解決事項を追記
review_due: YYYY-MM-DD    # 見直し期限を設定
updated: YYYY-MM-DD       # 常に最新の日付に
```

#### 3. draft から plan へ昇格
- 新ファイルを `docs/plan/` に作成
- `status: proposed` で開始
- `version: 1` を設定
- draft ファイルは削除または archive へ移送
- plan の `related_issues` に draft の背景 Issue を紐付け

#### 4. plan を実装中に更新
```yaml
updated: YYYY-MM-DD       # 常に最新の日付に
# status は proposed のままが多い（実装完了時に active へ）
```

#### 5. plan 実装完了時
```yaml
status: active            # 正式版に昇格
updated: YYYY-MM-DD       # 完了日を記録
```

#### 6. plan から intent へ移行
- 設計判断・背景の詳細を `docs/intent/` へ作成
- intent で `plan_reference` に plan のパスを明記
- plan の `references` に intent を逆参照で追加
- intent 承認後、plan を `docs/archives/` へ移送

#### 7. ドキュメント廃止・置き換え
```yaml
status: deprecated        # または superseded
superseded_by: <新plan のパス>  # 後継がある場合
updated: YYYY-MM-DD       # 廃止/置き換え日
```

### Status の遷移ルール

```
提案段階    実装段階            廃止段階
   ↓         ↓                  ↓
proposed → active → (deprecated / superseded)
   ↑                            ↑
   └────────────────────────────┘
  （計画見直し時に戻る可能性あり）
```

- **proposed**: 初期状態。検討中または昇格待ち
- **active**: 正式決定済み。実装中または実装完了
- **deprecated**: 廃止予定（後継なし）
- **superseded**: 新しいドキュメントに置き換わった

### Version の更新基準

- **マイナー更新**（例：typo 修正、説明の追加）→ `1.0` → `1.1`
- **メジャー更新**（例：スコープ変更、仕様大幅修正）→ `1.0` → `2.0`
- **破壊的変更**（例：API 仕様の非互換変更）→ `supersedes` フィールドで旧版を明記し、新ファイルを作成推奨

### トラブルシューティング

| 状況 | 対応 |
| --- | --- |
| draft が 30 日以上更新されていない | TTL Bot が Issue 起票。昇格 / 延長 / クローズを判断 |
| plan 承認前にアーカイブしてしまった | **ルール違反**。intent 承認後に改めて実行。PR で指摘されます |
| 複数の plan が同じ機能を記述している | 最新の plan をメインに、古い版は `superseded` に設定。archives へ移送 |
| guide/reference が古い情報を含んでいる | reference は `status: active` の plan/intent のみ反映。古い版との同期ズレは修正 PR で対応 |

```
