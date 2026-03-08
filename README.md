# SectorScope CLI

テーマ・セクター単位で米国株の騰落率を高速確認できるコマンドラインツール。

## 特徴

- **テーマ別の相対強弱** をすぐ把握（防衛、半導体、AI、農業など）
- **時価総額順でデフォルト表示**
- **複数出力形式**: テーブル / Markdown / JSON
- **ジャンル管理を分離**: 価格は外部ソース、テーマ分類は自前YAML管理
- 将来的に日本株にも対応予定

## インストール

```bash
git clone https://github.com/wataryoichi/sector-scope-cli.git
cd sector-scope-cli
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## クイックスタート

```bash
# ジャンル一覧
sectorscope list-sectors

# 防衛関連をデフォルト表示（時価総額降順）
sectorscope show defense

# 農業関連を年初来順で表示
sectorscope show agriculture --sort ytd

# Markdown テーブル出力
sectorscope show semiconductors --format markdown

# JSON 出力
sectorscope show ai --format json > ai.json

# 表示件数制限
sectorscope show defense --limit 5

# キャッシュ無効
sectorscope show defense --no-cache

# 昇順表示
sectorscope show semiconductors --sort 1d --asc
```

## 出力形式

### table（デフォルト）
Rich ベースの色付きテーブル。ターミナル向け。

### markdown
GitHub / Notion に貼れるテーブル形式。

```bash
sectorscope show defense --format markdown
```

出力例:
```
| Rank | Symbol | Name | Market Cap | Price | 1D | 1W | MTD | YTD | Volume |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | RTX | RTX Corporation | 164.2B | 132.45 | +1.2% | +4.8% | +5.1% | +12.4% | 5.2M |
```

### json
外部ツール連携用 JSON。

```bash
sectorscope show defense --format json | jq .
```

## ジャンル定義ファイル

`data/universe/us/` 以下にYAML形式で配置。

```yaml
id: defense
label: Defense
market: US
description: US listed defense and defense-adjacent companies
symbols:
  - RTX
  - LMT
  - NOC
  - GD
aliases:
  - military
tags:
  - defense
  - us
metadata:
  updated_at: "2026-03-08"
```

### なぜジャンル管理を分離しているか

Yahoo Finance 等のデータは便利だが、テーマ分類（軍事、農業、AI インフラなど）は安定して一貫提供されるとは限らない。そのため「価格は外部ソースから取得」「ジャンル所属は自前で管理」という構成を採用している。

## universe 管理

```bash
# 定義ファイルの検証
sectorscope universe validate
```

## ソートオプション

| キー | 説明 |
|---|---|
| `market_cap` | 時価総額（デフォルト） |
| `1d` | 前日比 |
| `1w` | 先週比 |
| `mtd` | 月初来 |
| `ytd` | 年初来 |
| `volume` | 出来高 |
| `symbol` | ティッカー |
| `name` | 企業名 |
| `price` | 株価 |

## 利用可能なジャンル（初期）

- `defense` - 防衛関連
- `semiconductors` - 半導体
- `ai` - AI関連
- `agriculture` - 農業関連
- `cybersecurity` - サイバーセキュリティ
- `nuclear` - 原子力・ウラン

## Notes on Yahoo Finance Data

- yfinance は Yahoo Finance の公開 API を使う OSS ライブラリであり、公式 SDK ではありません
- データの一時的な欠損やエラーが発生する可能性があります
- このツールは個人利用を想定しています。取得データの商用利用や大量再配布は Yahoo Finance の利用規約に抵触する可能性があります
- 本ツールの出力は投資助言ではありません。投資判断は自己責任で行ってください。本ツールの利用により生じた損害について、作者は一切の責任を負いません

## 注意事項

- これは投資助言ツールではなく、情報整理ツールです
- テーマ分類には恣意性があります
- 外部ソースのデータ欠損や遅延を前提に設計しています

## 技術スタック

- Python 3.11+
- Typer (CLI)
- Rich (テーブル表示)
- Pydantic (データモデル)
- yfinance (価格取得)
- pandas (集計)

## 将来の計画

- 日本株対応
- Vega-Lite 出力
- 複数ジャンル比較 (`compare`)
- AI 支援によるジャンルメンテナンス
- スクリーニング機能

## ライセンス

MIT
