# Documentation Operations Standards

Status: Proposed — pending rollout of automation phases.

## Purpose
- `docs/draft/` と `docs/plan/` を中心に、ドキュメント種別ごとの役割と運用境界を明確化する。
- 昇格・更新・廃止フローとレビュープロセスを標準化し、全メンバーが同じ基準で扱えるようにする。
- Front-matter スキーマ、テンプレート、CI を連携させ、ドキュメント品質と可観測性を高める。
- 一時ドキュメント（`draft`/`plan`/`survey`）から `intent`、そして `docs/archives/` への移行条件を厳格に定義し、棚卸しや監査を容易にする。

## Scope
- 対象: `docs/draft/`, `docs/plan/`, `docs/survey/`, およびそれらと連携する `intent/`, `guide/`, `reference/`, `archives/`。
- 適用範囲: ドキュメント作成・レビュー・承認・保守・自動化。
- 非対象: アプリケーションコードや API の実装規約（別 standards を参照）。

## Directory Roles
| パス | 目的 | 主な利用者 | 備考 |
| --- | --- | --- | --- |
| `docs/draft/` | アイデア、検討メモ、仮説、代替案等の一時保管 | 設計者・実装者・調査担当 | TTL管理（既定30日）。決定事項はここに残さない。 |
| `docs/plan/` | 合意済み仕様・実施計画の単一参照点 | 施策オーナー・レビュア・実装担当 | `plan/<domain>/<slug>/plan.md` を基本。version で履歴管理。 |
| `docs/intent/` | 設計判断・意思決定ログ | TL・設計レビュア | plan 更新時の根拠を格納。 |
| `docs/survey/` | 調査・検証レポート | 調査担当・意思決定者 | plan/intent から根拠として参照。 |
| `docs/guide/` / `docs/reference/` | 実装済み機能の運用ガイド・リファレンス | 全メンバー | plan の結果を反映。議論や検討は含めない。 |
| `docs/archives/` | intent 承認済みドキュメントの保管庫 | 監査担当・レビュア | intent 承認直後に移送。front-matter を保持したまま履歴保存。 |

## Lifecycle & Promotion Rules
1. **基本フロー**: `draft/survey → (survey) → plan → intent → (guide/reference) → archives`
2. **draft 運用**
   - `state`（`idea | exploring | paused`）で進行状況を明示。
   - `hypothesis`, `options`, `open_questions` を更新し、意思決定前の材料を整理。
   - `ttl_days`（既定30日）を超えた場合、Botが Issue を起票し、担当者は昇格/クローズ/延長を判断。
3. **plan 運用**
   - 合意済み仕様のみ。抽象的な検討や議論は `intent/` へ移す。
   - 破壊的変更や方針転換時は `version` を +1 し、`supersedes` / `superseded_by` で連結。
   - 非推奨になった計画は `status: deprecated` とし、後継 plan を `superseded_by` に明記。
4. **昇格ゲート (draft → plan)**
   - `scope` / `non_goals` が網羅的に記載されている。
   - `acceptance_criteria` が明確で測定可能。
   - 影響範囲（API, データ, 移行, セキュリティ, パフォーマンス, i18n/a11y）が洗い出されている。
   - `test_plan` と `observability` の方針が定義済み。
   - リスク分析と `rollback` 戦略が用意されている。
   - 関連 Issue / PR が front-matter で紐付いている。

## Temporary Document Governance
- `draft`、`plan`、`survey` は「開発過程専用の一時ドキュメント」であり、正式な `intent` に昇格していない状態でのアーカイブを禁止する。
- 一時ドキュメントの移行フロー:
  1. 一時ドキュメントを `intent` テンプレートへ再構成し、レビュワーから承認を得る。
  2. `intent` がマージまたは承認された直後に、該当一時ドキュメントのアーカイブ移送を行う。
  3. アーカイブ移送時は、元ディレクトリから原本を取り除き、`docs/archives/` へ同じ front-matter を保持したまま移す。
- 違反例:
  - `intent` 未承認のまま `docs/archives/` へ移動する。
  - アーカイブ後も元ディレクトリに原本を残す。
  - PR 説明やレビューコメントで移行内容を報告しない。
- レビュー時は、`intent` の承認状況、アーカイブ作業の報告、移動後ディレクトリのクリーンアップを必ず確認する。

## Archive Execution Checklist
1. `intent` が承認済みであることを確認し、PR 説明欄にリンクを明記する。
2. アーカイブ対象ドキュメントの front-matter を保持したまま `docs/archives/` へ移す。
3. 移行元ディレクトリのクリーンアップを差分で確認し、残骸がないことをレビュワーに示す。
4. アーカイブ対象と関連する `intent` を `related_prs` や `references` に追記し、相互リンクを更新する。
5. 必要に応じて `CHANGELOG.md` や関連 Issue へ作業ログを残す。

## Front-matter Schema
### 共通必須フィールド
| キー | 説明 |
| --- | --- |
| `title` | 文書タイトル（英語でシンプルに） |
| `domain` | 所属ドメイン（例: `order`, `infra`, `docs`） |
| `status` | `proposed | active | deprecated | superseded` |
| `version` | セマンティック or 整数のいずれか。更新時は+1。 |
| `created` / `updated` | `YYYY-MM-DD` 形式 |
| `related_issues` / `related_prs` | GitHub 番号配列（`[#123, ...]`） |
| `references` | survey/intent/guide/reference 等への相対リンク |

### draft 専用フィールド
| キー | 説明 |
| --- | --- |
| `state` | `idea | exploring | paused` |
| `hypothesis` | 検証したい仮説（リスト可） |
| `options` | 代替案（比較表可） |
| `open_questions` | 未解決事項 |
| `next_action_by` | 次アクション担当者 |
| `review_due` | 見直し期限（`YYYY-MM-DD`） |
| `ttl_days` | 自動失効までの日数（既定30） |

### plan 専用フィールド
| キー | 説明 |
| --- | --- |
| `scope` / `non_goals` | 対象としない領域まで明文化 |
| `requirements` | `functional` / `non_functional` に分類 |
| `constraints` | 技術・組織的制約 |
| `api_changes`, `data_models`, `migrations` | 該当がない場合は空配列 |
| `rollout_plan` | フェーズ定義 / exit criteria |
| `rollback` | 失敗時の戻し方針 |
| `test_plan` | `unit`, `integration`, `e2e` などの戦略 |
| `observability` | ログ・メトリクス・アラートの方針 |
| `security_privacy` | 機密情報の取り扱い方針 |
| `performance_budget` | 許容指標（例: CI実行時間 ≤5分） |
| `i18n_a11y` | 多言語・アクセシビリティ配慮の要件 |
| `acceptance_criteria` | 完了を判断するための条件 |
| `supersedes` / `superseded_by` | 旧/新 plan との関係（任意） |

## Review & Approval Workflow
1. **PR テンプレート**
   - draft: 目的 / 仮説 / 期限 / 担当のチェックリストを記入。
   - plan: 昇格ゲート項目を全て Yes/No で確認。
   - intent: 承認後に実施するアーカイブ対象を明記し、移行後の差分を提示。
2. **レビュア割当**
   - ドメイン CODEOWNERS に自動リクエスト。
   - 影響領域（`infra`, `core`, `shared`など）の代表者を追加アサイン。
   - plan は **最低2名承認** が必要。draft は **1名 or 自己承認可**。intent は **アーカイブ対象に関連する担当者** を含める。
3. **マージ後運用**
   - plan 作成/更新時は GitHub Issues に Epic を作成 or 紐付け、front-matter の `related_issues` と相互リンク。
   - 更新内容が意志決定を伴う場合は `docs/intent/` に ADR を追加し、plan から参照。
   - intent 承認後、即座にアーカイブチェックリストを実行し、必要な差分を同一 PR で完了させる。

## Automation Roadmap
| フェーズ | 対応範囲 | 成果物 |
| --- | --- | --- |
| Phase 0 | 指針合意とテンプレート草案共有 | 本 standards / plan 承認、Epic 登録 |
| Phase 1 | draft/plan/intent テンプレート + PRチェックリスト整備 | `docs/_templates/` と `.github/pull_request_template.md` 更新 |
| Phase 2 | lint + link-check を CI へ導入 | `markdownlint-cli2`, `lycheeverse/lychee` を GitHub Actions で実行 |
| Phase 3 | Front-matter 検証 + stale draft Bot | JSON Schema 検証 & `ttl_days` 超過通知の自動化 |
| Phase 4 | intent 承認後のアーカイブ自動チェック | CI で `docs/archives/` への移送と移行元削除を検証 |

## Observability & Metrics
- CI 成功率と平均実行時間を週次でレビュー。閾値超過時は改善Issueを起票。
- stale draft Bot の Issue 数 / 平均対応時間を月次で集計し、TTL の妥当性を評価。
- intent 承認後のアーカイブ実施率、違反検知件数、修正リードタイムを Docs Platform WG がモニタリングする。
- plan 更新時は `updated` を必須更新し、`intent/` と `archives/` の整合性を確認する。

## Risk Management
| リスク | 影響 | 対応策 |
| --- | --- | --- |
| テンプレート変更による負荷増 | 変更作業が停滞 | ガイド付きチュートリアルとサンプル提供。初回はサポートレビューを実施。 |
| CI 遅延 | 開発フロー停滞 | lint / link-check の並列化、キャッシュ活用。5分超過で段階的にロールバック。 |
| Front-matter 移行の失敗 | 旧planとの互換性問題 | 移行期間は警告モード。30日間は旧フォーマットを許容。 |
| stale Bot の過検知 | 不要なチケット増加 | 初期 TTL は60日に設定し、実データを基に調整。 |
| intent 承認前のアーカイブ | 情報の欠落・レビュー漏れ | PR テンプレートと CI で intent リンク必須チェックを追加。 |

## Compliance Rules
- ドキュメントに秘密情報・個人情報を含めない。環境値は `.env.example` を参照。
- CI ログ出力にはマスク設定を適用し、機密情報が残らないようにする。
- 公開資料として扱える品質を前提に、OSS 化を想定した文言に統一する。
- intent 承認後のみアーカイブできるルールを遵守し、違反が確認された PR はレビュワーがブロックする。

## Maintenance Checklist
- [ ] `docs/_templates/` に draft / plan / intent テンプレートを追加し、最新スキーマを反映。
- [ ] PR テンプレートのチェックリストを更新し、CODEOWNERS へ告知。
- [ ] lint + link-check 用 GitHub Actions を導入し、しきい値を監視。
- [ ] front-matter JSON Schema を整備し、CI へ組み込む。
- [ ] stale draft Bot（ttl_days判定）の PoC を完了し、運用プロセスを文書化。
- [ ] intent 承認後のアーカイブ自動検証ワークフローを設計し、CI へ段階的に導入。

---
本 standards は `documentation_operations_policy` Plan を具現化するための実務規約であり、Plan の更新に応じて本書も改訂する。変更時は `Status` と `updated` 日付を必ず更新すること。
