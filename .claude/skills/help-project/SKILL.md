---
name: help-project
description: このプロジェクトで使う推奨コマンド、スキル、開始方法、運用ルールを案内する
tools: Read,LS,Glob
---

# /help-project

このスキルは、このプロジェクト専用の「使い方ガイド」です。

## まず覚えるコマンド

### 推奨開始コマンド
- `/start-dev`
  - `docs/spec.md`、`TODO.md`、`docs/handoff-current.md` を確認してから作業開始します。

### Claude Code の基本操作で覚えやすいもの
- `/help`
  - Claude Code 全体の組み込みヘルプを表示します。
- `/compact`
  - 会話を圧縮してコンテキストを整理します。
- `/doctor`
  - 設定や環境の問題を診断します。
- `/bug`
  - 問題報告に使います。
- `/clear`
  - 現在の会話をクリアします。

> 注意: 組み込みコマンドは Claude Code のバージョンや環境で表示差異があります。`/` を入力すると、その環境で利用可能なコマンド候補を一覧できます。

## このプロジェクトでの基本運用
1. `/start-dev` を実行
2. `docs/spec.md` を前提に実装
3. 実装後に `TODO.md` を更新
4. 中断時は `docs/handoff-current.md` を更新
5. 区切りでコミット候補を整理

## よく使う自然言語プロンプト例
- `docs/spec.md を読んで、最初に着手すべきタスクを提案して`
- `TODO.md を見て、未完了タスクを優先順位つきで整理して`
- `この変更で docs/spec.md の更新が必要か判定して`
- `実装前に影響ファイルを洗い出して`
- `作業の最後に handoff を更新して`

## このプロジェクトの重要ファイル
- `docs/spec.md` - 完全仕様
- `TODO.md` - 実装タスク一覧
- `docs/handoff-current.md` - セッション引き継ぎ
- `CLAUDE.md` - 常時ルール
- `.claude/skills/start-dev/SKILL.md` - 開始用スキル
- `.claude/skills/help-project/SKILL.md` - このガイド

## ユーザーへの案内ルール
- 使い方を聞かれたら、まず `/help-project` を案内する。
- 開発開始依頼なら、まず `/start-dev` を案内する。
- Claude Code 標準機能の質問は、必要に応じて `/help` や `/doctor` も案内する。

## 案内メッセージ例
- `まず /start-dev を実行してください。仕様と TODO を確認してから開始できます。`
- `使えるコマンドを忘れたら / と入力して候補一覧を見るか、/help-project を実行してください。`
- `Claude Code 自体の標準コマンドは /help で確認できます。`
