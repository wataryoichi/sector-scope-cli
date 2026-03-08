# SectorScope CLI 仕様書

最終更新: 2026-03-08

## 1. 概要

**SectorScope CLI** は、米国株・日本株の銘柄群を「ジャンル（テーマ / セクター / 業種バスケット）」単位で一覧表示し、以下のような騰落率を高速に確認できるコマンドラインツールである。

- 前日比
- 先週比
- 月初来
- 年初来
- 任意期間比
- 必要に応じて時価総額や売買代金、ティッカー順などで並び替え

初期フェーズでは **米国株を先行実装** とし、将来的に日本株（TSE、ETF 含む）へ拡張できる構成にする。

本ツールは単なる価格ビューアではなく、**「銘柄ユニバース管理」** と **「価格集計・出力」** を分離した設計とし、ジャンル単位の定期メンテナンスが行えることを重視する。

---

## 2. 目的

### 2.1 ユーザー価値
- 農業、軍事、半導体、電力、AI など、**テーマ別の相対強弱** をすぐ把握できる
- 米国株の一覧を **時価総額順でデフォルト表示** できる
- CLI だけでなく **Markdown テーブル** や **Vega-Lite JSON** でも出力できる
- 将来、ブログ、レポート、Notebook、Markdown 拡張表示へ流用しやすい

### 2.2 解決したい課題
- Yahoo Finance 等のデータは便利だが、**テーマ分類が安定して一貫提供されるとは限らない**
- そのため「価格は外部ソースから取得」「ジャンル所属は自前ユニバースでも保守可能」という構成が必要
- 銘柄数が増えると、手作業でのバスケット維持が面倒になるため、定期更新フローも必要

---

## 3. プロジェクト名・ツール名

## 3.1 採用名
- **GitHub Project 名**: `sector-scope-cli`
- **CLI コマンド名**: `sectorscope`

### 3.2 命名理由
- 「Sector」だけでなく、軍事・農業・AI のような**テーマ群**も扱うため `Scope` が相性良い
- CLI 名が短く、README やコマンド例を書きやすい
- 将来的に US / JP 両対応しても名称がブレにくい

### 3.3 代替案
- `theme-tape-cli`
- `market-basket-cli`
- `sector-board`
- `market-scan-cli`

---

## 4. 対象市場・スコープ

### 4.1 初期スコープ（MVP）
- 米国株のみ
- 普通株を優先
- 必要に応じて ETF は明示的にジャンルに含められる
- 出力形式:
  - table（CLI向け整形）
  - markdown
  - json
  - vega-lite
- 並び順:
  - market_cap desc（デフォルト）
  - pct_change desc/asc
  - symbol
  - name
  - volume
  - custom rank

### 4.2 次期スコープ
- 日本株対応
- 日本株コード + サフィックス（例: `7203.T`）への対応
- 為替換算オプション
- マルチジャンル同時比較
- 上位 / 下位 n 件の抽出
- スパークラインや期間比較チャート

### 4.3 非スコープ（MVP時点）
- リアルタイム約定データの保証
- 完全自動の正確なテーマ分類
- 取引機能
- Web UI
- DB を必須とする重い構成

---

## 5. 想定ユースケース

### 5.1 例
- 防衛関連の米国株を時価総額順で見る
- 農業関連の前日比ランキングを見る
- AI / 半導体 / 電力の3ジャンルを別々に Markdown 表で出す
- 生成した JSON をそのままブログやレポート作成に使う
- Vega-Lite 対応 Markdown 環境で、ジャンル内の年初来騰落率を可視化する

### 5.2 利用イメージ
```bash
sectorscope list-sectors
sectorscope show defense
sectorscope show agriculture --sort ytd --limit 20
sectorscope show ai --format markdown
sectorscope show semiconductors --format vega-lite --metric ytd
sectorscope compare defense energy grid --format markdown
sectorscope universe validate
sectorscope universe refresh --source auto
```

---

## 6. 主要要件

## 6.1 機能要件
1. ジャンル一覧を表示できる
2. 指定ジャンルの銘柄一覧を取得できる
3. 前日比、先週比、月初来、年初来、任意期間比を計算できる
4. デフォルトは時価総額降順
5. 並び順をオプションで変更できる
6. 出力形式を切り替えられる
7. ジャンル定義ファイルをローカル管理できる
8. ジャンル所属銘柄のメンテナンス支援コマンドを持つ
9. 価格取得失敗時や欠損時のフォールバック表示ができる
10. 将来的な日本株対応に備えて市場差分を抽象化する

## 6.2 非機能要件
- 小型環境でも動くこと
- キャッシュを前提に API 呼び出し数を抑えること
- 出力が安定し、他ツールから利用しやすいこと
- テストしやすいこと
- README の例が豊富で、初見ユーザーが迷わないこと

---

## 7. 価格・指標の定義

## 7.1 基本指標
各銘柄について最低限以下を扱う。

- `symbol`
- `name`
- `exchange`
- `currency`
- `sector`（外部ソース由来があれば）
- `industry`（外部ソース由来があれば）
- `market_cap`
- `regular_market_price`
- `prev_close`
- `week_ago_close`
- `month_start_close`
- `year_start_close`
- `volume`
- `avg_volume`

## 7.2 騰落率計算
- `1d = (current / prev_close - 1) * 100`
- `1w = (current / week_ago_close - 1) * 100`
- `mtd = (current / month_start_close - 1) * 100`
- `ytd = (current / year_start_close - 1) * 100`
- 任意期間も同様

### 7.2.1 営業日補正
- 先週比は「厳密な7日前」ではなく、**基準日の直近利用可能営業日終値**
- 年初来は、当年最初の取引日の終値を用いる
- データ欠損時は `null` とし、表示時は `—`

---

## 8. ジャンル設計

## 8.1 用語
本仕様では「ジャンル」を以下の総称として扱う。

- Yahoo / provider の sector
- industry
- 自前テーマ（例: defense, agriculture, AI infrastructure, uranium, robotics）

つまり、**実体は「銘柄バスケット」** であり、ラベルがジャンルになる。

## 8.2 初期実装で持つ代表ジャンル例
- defense
- agriculture
- semiconductors
- ai
- ai-infrastructure
- utilities
- grid
- nuclear
- uranium
- oil-gas
- cybersecurity
- robotics
- biotech
- industrials
- shipping
- aerospace
- data-center
- rare-earth
- lithium

## 8.3 ジャンル定義ファイル
ジャンルの実体は、Git 管理可能な YAML / JSON ファイルで持つ。

推奨:
- `data/universe/us/*.yaml`
- `data/universe/jp/*.yaml`

例:
```yaml
id: defense
label: Defense
market: US
description: US listed defense and defense-adjacent companies
maintainer: manual+auto
symbols:
  - RTX
  - LMT
  - NOC
  - GD
  - LHX
  - AVAV
aliases:
  - military
  - aerospace-defense
tags:
  - defense
  - military
  - us
metadata:
  source_priority:
    - manual
    - auto-yfinance
  updated_at: 2026-03-08
```

## 8.4 ジャンルの分類レイヤ
1. **Manual curated**
   - 最も信頼
   - オーナーが調整可能
2. **Auto suggested**
   - 外部データから候補提案
   - そのまま採用しない
3. **AI assisted maintenance**
   - 候補の整形、説明生成、差分レビュー支援
4. **Runtime overlay**
   - コマンド実行時の一時バスケット

---

## 9. データソース戦略

## 9.1 基本方針
価格・時価総額・企業名などは主に `yfinance` を利用する。
ただし、**業種 / テーマ所属の完全自動化は信用しすぎない**。

## 9.2 理由
- 価格系列の取得は `yfinance` で比較的実装しやすい
- 一方で `Ticker.info` 系はフィールドの揺れや欠損があり得るため、ジャンル分類の単一ソースとしては危険
- よって、**「市場データ取得」と「ジャンル所属管理」を分離** する

## 9.3 ソース優先順位
### 価格系
1. yfinance
2. ローカルキャッシュ
3. 失敗時は前回スナップショット

### メタデータ系
1. 手動 universe 定義
2. yfinance 由来 metadata
3. AI 補助生成メタ情報

---

## 10. アーキテクチャ

## 10.1 推奨技術スタック
- Python 3.11+
- `typer` または `click` で CLI 実装
- `rich` で CLI テーブル表示
- `pydantic` で設定・出力モデル定義
- `yfinance` で価格取得
- `pandas` で集計
- `pyyaml` で universe 定義読込
- `platformdirs` でキャッシュ保存先管理
- `orjson`（任意）で高速 JSON 出力
- `pytest` でテスト

## 10.2 ディレクトリ構成案
```text
sector-scope-cli/
├─ CLAUDE.md
├─ README.md
├─ pyproject.toml
├─ TODO.md
├─ docs/
│  ├─ spec.md
│  ├─ handoff-current.md
│  ├─ cli-examples.md
│  └─ maintenance-playbook.md
├─ src/
│  └─ sectorscope/
│     ├─ __init__.py
│     ├─ cli.py
│     ├─ config.py
│     ├─ models/
│     │  ├─ quote.py
│     │  ├─ universe.py
│     │  └─ output.py
│     ├─ providers/
│     │  ├─ base.py
│     │  ├─ yfinance_provider.py
│     │  └─ cache.py
│     ├─ services/
│     │  ├─ metrics.py
│     │  ├─ sorting.py
│     │  ├─ formatter.py
│     │  ├─ universe_service.py
│     │  └─ maintenance_service.py
│     ├─ formatters/
│     │  ├─ table.py
│     │  ├─ markdown.py
│     │  ├─ json_fmt.py
│     │  └─ vega_lite.py
│     └─ assets/
│        └─ prompts/
│           └─ universe-maintenance.md
├─ data/
│  └─ universe/
│     ├─ us/
│     │  ├─ defense.yaml
│     │  ├─ agriculture.yaml
│     │  └─ ...
│     └─ jp/
├─ tests/
│  ├─ test_metrics.py
│  ├─ test_universe_loading.py
│  ├─ test_sorting.py
│  ├─ test_markdown_output.py
│  └─ test_vega_lite_output.py
└─ scripts/
   ├─ refresh_universe.py
   └─ benchmark_cli.py
```

---

## 11. CLI コマンド仕様

## 11.1 `list-sectors`
ジャンル一覧を表示する。

### 例
```bash
sectorscope list-sectors
sectorscope list-sectors --market us
sectorscope list-sectors --format json
```

### 出力項目
- `id`
- `label`
- `market`
- `symbol_count`
- `description`
- `updated_at`

---

## 11.2 `show`
指定ジャンルの銘柄一覧を表示する。

### 例
```bash
sectorscope show defense
sectorscope show agriculture --sort market_cap
sectorscope show semiconductors --sort ytd --desc
sectorscope show ai --format markdown
sectorscope show defense --columns symbol,name,market_cap,1d,1w,ytd
sectorscope show defense --limit 15
sectorscope show defense --as-of 2026-03-07
```

### 主なオプション
- `--market us|jp`
- `--sort market_cap|1d|1w|mtd|ytd|symbol|name|volume|custom`
- `--desc / --asc`
- `--format table|markdown|json|vega-lite`
- `--limit N`
- `--columns ...`
- `--as-of YYYY-MM-DD`
- `--cache/--no-cache`
- `--price-source yfinance`
- `--include-etf`
- `--exclude-missing`

---

## 11.3 `compare`
複数ジャンルを比較表示する。

### 例
```bash
sectorscope compare defense agriculture semiconductors
sectorscope compare defense ai-infrastructure grid --metric ytd
sectorscope compare defense agriculture --format markdown
```

### MVP では最低限以下をサポート
- 各ジャンルの代表統計
  - 銘柄数
  - 時価総額合計（取得できた分）
  - 平均 1d / 1w / ytd
  - 上位銘柄
- 将来はジャンル横断ヒートマップへ拡張

---

## 11.4 `universe validate`
ジャンル定義ファイルを検証する。

### 検証内容
- 重複 symbol
- 不正 market
- 空 symbols
- フォーマットエラー
- alias 重複
- 存在しない参照

---

## 11.5 `universe refresh`
ジャンル更新支援。

### モード
- `--source auto`
  - yfinance metadata などから補助情報取得
- `--source manual`
  - 手動ファイルのみ整形
- `--source ai`
  - AI 用プロンプトを出力し、差分レビュー素材を生成

### 例
```bash
sectorscope universe refresh --market us --source auto
sectorscope universe refresh defense --source ai
sectorscope universe refresh agriculture --write-suggestions
```

---

## 11.6 `universe suggest`
新規候補の提案を作る。

### 例
```bash
sectorscope universe suggest defense
sectorscope universe suggest nuclear --from-query "uranium mining us listed"
```

### 出力
- 候補 symbol
- 企業名
- 既知の sector / industry
- 候補理由
- confidence
- manual review required

---

## 11.7 `schema`
利用可能オプションや出力スキーマを確認する。

### 例
```bash
sectorscope schema sectors
sectorscope schema output-json
sectorscope schema vega-lite
```

---

## 12. 出力仕様

## 12.1 table
`rich` ベースの CLI 向け表示。

### 表示カラム例
- Rank
- Symbol
- Name
- Market Cap
- Price
- 1D
- 1W
- MTD
- YTD
- Volume

### 表示ルール
- 数値は桁区切り
- パーセントは小数点 1〜2 桁
- 欠損値は `—`
- 大きい値の単位略記:
  - 1.2T
  - 532B
  - 9.8M

## 12.2 markdown
GitHub / Notion / Markdown Viewer 向けテーブル。

### 例
```md
| Rank | Symbol | Name | Market Cap | 1D | 1W | YTD |
|---:|---|---|---:|---:|---:|---:|
| 1 | LMT | Lockheed Martin | 106.2B | 1.2% | 4.8% | 12.4% |
```

## 12.3 json
外部ツール連携用。

### 例
```json
{
  "meta": {
    "tool": "sectorscope",
    "market": "US",
    "sector_id": "defense",
    "as_of": "2026-03-07",
    "sort": "market_cap",
    "order": "desc"
  },
  "items": [
    {
      "rank": 1,
      "symbol": "LMT",
      "name": "Lockheed Martin",
      "market_cap": 106200000000,
      "price": 451.23,
      "pct_1d": 1.2,
      "pct_1w": 4.8,
      "pct_mtd": 5.1,
      "pct_ytd": 12.4
    }
  ]
}
```

## 12.4 vega-lite
可視化用 JSON を出力。

### 想定チャート
1. ジャンル内の YTD 横棒グラフ
2. 時価総額 vs YTD 散布図
3. 1D / 1W / YTD の grouped bar
4. compare 時のジャンル別平均騰落率

### 例（横棒）
```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "data": {"values": []},
  "mark": "bar",
  "encoding": {
    "y": {"field": "symbol", "type": "nominal", "sort": "-x"},
    "x": {"field": "pct_ytd", "type": "quantitative"},
    "tooltip": [
      {"field": "symbol", "type": "nominal"},
      {"field": "name", "type": "nominal"},
      {"field": "pct_ytd", "type": "quantitative"}
    ]
  }
}
```

---

## 13. 並び順仕様

## 13.1 デフォルト
- `market_cap desc`

## 13.2 サポート順序
- `market_cap`
- `price`
- `1d`
- `1w`
- `mtd`
- `ytd`
- `volume`
- `avg_volume`
- `symbol`
- `name`
- `custom`

## 13.3 custom
ジャンル定義ファイル内に `rank_overrides` を持てるようにする。

例:
```yaml
rank_overrides:
  AVAV: 1
  LMT: 2
  RTX: 3
```

利用例:
```bash
sectorscope show defense --sort custom
```

---

## 14. キャッシュ仕様

## 14.1 目的
- Yahoo 側への過剰アクセス防止
- Raspberry Pi でも体感速度を確保
- 同一日の再実行を高速化

## 14.2 保存単位
- symbol 単位の metadata キャッシュ
- symbol + period 単位の price history キャッシュ
- sector show の整形済み結果キャッシュ（任意）

## 14.3 TTL 案
- metadata: 7日
- 当日価格: 5〜15分
- 日足履歴: 1日
- universe suggestions: 7日

## 14.4 保存場所
- `~/.cache/sectorscope/` を基本
- Windows / macOS / Linux は `platformdirs` で吸収

---

## 15. ジャンルメンテナンス仕様

## 15.1 背景
yfinance 等から企業メタ情報は取得できても、テーマ投資的な「軍事」「農業」「送電網」「AI データセンター」などの分類は**人間が定義する方が実務上強い**。

## 15.2 方針
- 正式 universe は Git 管理
- 自動処理は「候補提案」に留める
- 最終採用はレビュー必須

## 15.3 メンテナンスの3方式
### A. 手動更新
- YAML を直接編集
- 最も確実

### B. 自動補助更新
- 既存 symbol から sector / industry / company summary を取得
- 類似銘柄候補を提案
- 例: `defense` に対して aerospace & defense 近傍銘柄候補を出す

### C. AI 支援更新
- AI に投げるための structured prompt と JSON スキーマを assets に保存
- AI 出力を `suggestions/*.json` に格納
- 人間がレビューして universe に反映

## 15.4 AI 支援用成果物
以下をプロジェクトに含める。

- `src/sectorscope/assets/prompts/universe-maintenance.md`
- `schemas/universe_suggestion.schema.json`

---

## 16. AI 連携の仕様

## 16.1 目的
yfinance で完結しないテーマ銘柄メンテナンスを、AI モデルに安全に補助させる。

## 16.2 AI に要求する出力
- テーマ名
- 候補銘柄
- 候補理由
- 除外理由
- confidence
- human_review_required
- 出典メモ欄（URL 文字列ではなく参照メモでも可）

## 16.3 推奨 JSON スキーマ
```json
{
  "sector_id": "defense",
  "generated_at": "2026-03-08T00:00:00Z",
  "market": "US",
  "candidates": [
    {
      "symbol": "LHX",
      "name": "L3Harris Technologies",
      "action": "keep",
      "confidence": 0.96,
      "reason": "Major US defense contractor with direct exposure to military communications and ISR.",
      "human_review_required": true
    },
    {
      "symbol": "XYZ",
      "name": "Example Corp",
      "action": "add",
      "confidence": 0.52,
      "reason": "Adjacent exposure only; verify if theme inclusion is appropriate.",
      "human_review_required": true
    }
  ]
}
```

## 16.4 AI 連携時のルール
- AI の提案を universe に自動反映しない
- 低 confidence を警告表示する
- 既存除外リストを尊重する
- `manual_review_required` を必須にする

---

## 17. データモデル

## 17.1 UniverseDefinition
```python
class UniverseDefinition(BaseModel):
    id: str
    label: str
    market: Literal["US", "JP"]
    description: str | None = None
    symbols: list[str]
    aliases: list[str] = []
    tags: list[str] = []
    metadata: dict = {}
```

## 17.2 QuoteSnapshot
```python
class QuoteSnapshot(BaseModel):
    symbol: str
    name: str | None = None
    currency: str | None = None
    exchange: str | None = None
    market_cap: int | None = None
    price: float | None = None
    prev_close: float | None = None
    close_1w_ref: float | None = None
    close_mtd_ref: float | None = None
    close_ytd_ref: float | None = None
    volume: int | None = None
    avg_volume: int | None = None
```

## 17.3 OutputRow
```python
class OutputRow(BaseModel):
    rank: int
    symbol: str
    name: str | None = None
    market_cap: int | None = None
    price: float | None = None
    pct_1d: float | None = None
    pct_1w: float | None = None
    pct_mtd: float | None = None
    pct_ytd: float | None = None
    volume: int | None = None
```

---

## 18. エラーハンドリング

### 想定ケース
- シンボルが取得不能
- 上場廃止
- 時価総額が null
- 価格履歴が不足
- ソースの一時障害
- ジャンルファイルが破損
- `vega-lite` 出力対象が空

### 方針
- 1銘柄失敗で全体を落とさない
- `warnings` を標準エラーまたは JSON meta に含める
- `--strict` 指定時のみ失敗扱いにできる

---

## 19. パフォーマンス要件

## 19.1 目安
- 10〜30 銘柄のジャンル表示: 快適
- 100 銘柄程度: 許容
- compare で複数ジャンル: キャッシュ前提で実用的

## 19.2 Raspberry Pi 対応の考え方
### 結論
- **Raspberry Pi 4 / 5 なら十分現実的**
- **Raspberry Pi Zero でも不可能ではないが、快適性はかなり低い**

### 理由
- 計算自体は軽い
- 重いのはネットワーク I/O と pandas / yfinance の初期処理
- キャッシュを活かせば低スペックでも使える
- Zero 系では大量銘柄の連続 fetch が遅く、保守用途には不向き

## 19.3 想定環境の目安
### 快適
- Python 3.11+
- RAM 2GB 以上
- SSD or 高速ストレージ
- Raspberry Pi 4 / 5
- Mac / Linux / WSL

### 最低限
- RAM 512MB〜1GB
- Zero 系は少量ジャンル、キャッシュ前提
- 出力形式は table / json 中心
- vega-lite 生成自体は軽いが、大量データ処理時は待つ可能性あり

---

## 20. README に必ず含めるべき内容

1. 何ができるツールか
2. なぜジャンル管理を分離しているか
3. インストール方法
4. 最速スタート
5. 典型コマンド例
6. 出力形式別の例
7. ジャンル定義ファイルの書き方
8. universe refresh / validate の使い方
9. AI 補助メンテナンスの流れ
10. トラブルシュート
11. 将来の日本株対応方針

---

## 21. README のコマンド例（必須サンプル）

```bash
# ジャンル一覧
sectorscope list-sectors

# 防衛関連をデフォルト表示（時価総額降順）
sectorscope show defense

# 農業関連を年初来順で表示
sectorscope show agriculture --sort ytd --desc

# Markdown テーブル出力
sectorscope show semiconductors --format markdown

# JSON 出力
sectorscope show ai-infrastructure --format json > ai.json

# Vega-Lite 出力
sectorscope show defense --format vega-lite --metric ytd > defense-ytd.vl.json

# 複数ジャンル比較
sectorscope compare defense agriculture grid

# universe 定義の検証
sectorscope universe validate

# 自動補助更新
sectorscope universe refresh --market us --source auto

# AI 補助候補の生成
sectorscope universe refresh defense --source ai
```

---

## 22. テスト方針

## 22.1 単体テスト
- 騰落率計算
- 営業日補正
- ソート順
- 欠損値表示
- Markdown 出力整形
- Vega-Lite JSON 妥当性
- UniverseDefinition パース

## 22.2 結合テスト
- yfinance provider モック
- `show` コマンド end-to-end
- `list-sectors` 出力検証
- `universe validate` の異常系

## 22.3 フィクスチャ
- 固定 price history JSON
- テスト用 universe YAML
- 欠損データケース
- market_cap null ケース

---

## 23. セキュリティ・運用注意

- 投資助言ツールではなく、情報整理ツールとして位置づける
- 外部ソースのデータ欠損や遅延を前提に扱う
- テーマ分類は恣意性があるため README に明記
- AI 提案の自動反映は禁止

---

## 24. 実装優先順位

## Phase 1
- US universe 読込
- `list-sectors`
- `show`
- 1d / 1w / mtd / ytd
- sort
- table / markdown / json
- キャッシュ基盤

## Phase 2
- `compare`
- `vega-lite`
- `universe validate`
- `universe refresh --source auto`
- README 充実

## Phase 3
- AI maintenance prompt / schema
- `universe suggest`
- `custom sort`
- スナップショット保存

## Phase 4
- JP market 対応
- 日本株コード体系対応
- 為替換算
- compare の強化

---

## 25. Claude Code への実装依頼時の重点指示

1. まず MVP を完成させる
2. provider 層と universe 層を分離する
3. README を同時並行で厚く書く
4. CLI の `--help` を丁寧にする
5. 失敗時でも全体を落としにくい実装にする
6. AI 連携は「提案のみ」で自動反映しない
7. 将来の日本株対応を見越して market 抽象を入れる
8. 出力モデルを固定し、Markdown / JSON / Vega-Lite の整合性を保つ

---

## 26. 受け入れ基準

### MVP 完了条件
- `sectorscope list-sectors` が動く
- `sectorscope show defense` が動く
- デフォルトで時価総額降順になる
- `--sort ytd` などが機能する
- `--format markdown/json` が機能する
- 欠損値で落ちない
- README に 15 以上の実行例がある
- `docs/spec.md` と実装が矛盾しない

---

## 27. 補足: yfinance を使う際の実務判断

- price history の主用途には適している
- company metadata は便利だが揺れがある前提で扱う
- sector / industry は補助情報に留める
- テーマ銘柄群は curated universe を主とする方が長期的に安定

---

## 28. 参考実装メモ

### 28.1 価格取得の最小フロー
1. universe から symbols を読む
2. まとめて履歴取得
3. 基準日 close を抽出
4. 騰落率算出
5. metadata をマージ
6. sort
7. formatter へ渡す

### 28.2 Markdown との相性
- GitHub README にそのまま貼れる
- ブログ下書きや投資メモに流用しやすい
- compare 結果をそのまま共有しやすい

### 28.3 Vega-Lite との相性
- JSON だけで可視化定義を持てる
- Markdown 拡張や埋め込み UI に再利用しやすい
- ツール本体は描画せず、仕様を出力するだけでよい

---

## 29. 将来拡張アイデア

- `--sparklines ascii`
- セクター全体の equal-weight / market-cap-weight 指数生成
- `--top` / `--bottom`
- `--screen "market_cap>10B and ytd>0"`
- CSV / clipboard 出力
- 日次スナップショットの蓄積と差分比較
- ニュース要約連携
- 日本株 / 米国株を横断したテーマ比較

---

## 30. 参考リンク
- yfinance (PyPI)
- Vega-Lite Documentation
- Vega-Lite Example Gallery
