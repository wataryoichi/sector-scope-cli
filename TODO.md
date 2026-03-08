# TODO

## Phase 1 (MVP) — 初期実装

- [x] プロジェクト基盤（pyproject.toml、ディレクトリ構成）
- [x] データモデル（UniverseDefinition, QuoteSnapshot, OutputRow）
- [x] Universe 読込サービス
- [x] yfinance プロバイダ + キャッシュ基盤
- [x] 騰落率計算（1d/1w/mtd/ytd）
- [x] ソートサービス（market_cap, ytd, symbol 等）
- [x] フォーマッタ（table/markdown/json）
- [x] CLI コマンド（list-sectors, show, universe validate）
- [x] サンプル universe YAML（defense, semiconductors, ai, agriculture, cybersecurity, nuclear）
- [x] テスト（22件: metrics, sorting, universe, markdown, json）
- [x] README.md

## Phase 2 — 機能拡張

- [ ] `compare` コマンド実装
- [ ] `vega-lite` 出力フォーマッタ
- [ ] `universe refresh --source auto` 実装
- [ ] 追加 universe YAML（oil-gas, robotics, biotech, shipping, rare-earth 等）
- [ ] `--columns` オプション対応
- [ ] `--as-of` オプション対応
- [ ] `--include-etf` / `--exclude-missing` オプション

## Phase 3 — AI 連携・拡張

- [ ] AI maintenance prompt / schema
- [ ] `universe suggest` コマンド
- [ ] `custom` ソート（rank_overrides 対応済み、CLI統合）
- [ ] スナップショット保存

## Phase 4 — 日本株対応

- [ ] JP market 対応
- [ ] 日本株コード体系（7203.T 等）
- [ ] 為替換算
- [ ] compare の強化
