# ハンドオフノート - 2026-03-08

## 現在の状態
- Phase 1 (MVP) が完成
- `list-sectors`, `show`, `universe validate` コマンドが動作
- table / markdown / json 出力対応
- 6つのジャンル定義 YAML（defense, semiconductors, ai, agriculture, cybersecurity, nuclear）
- 22件のテストが全て通過
- yfinance からリアルタイムデータ取得 + ファイルキャッシュ

## 次にやること（優先順）
1. Phase 2: `compare` コマンドの実装
2. Phase 2: `vega-lite` 出力フォーマッタ
3. Phase 2: 追加 universe YAML の作成
4. Phase 2: `--columns`, `--as-of` オプション

## 重要な注意事項・決定事項
- yfinance はまとめて履歴取得（`yf.download`）→ メタデータは個別取得（`Ticker.info`）
- ソートで None は常に末尾に配置
- キャッシュは `~/.cache/sectorscope/` にJSON形式で保存
- `data/universe/us/*.yaml` がジャンル定義の実体

## 関連ファイル
- `src/sectorscope/cli.py` - CLI メインエントリポイント
- `src/sectorscope/providers/yfinance_provider.py` - 価格取得
- `src/sectorscope/services/` - ビジネスロジック
- `src/sectorscope/formatters/` - 出力フォーマッタ
- `data/universe/us/` - ジャンル定義
- `tests/` - テスト
