"""Universe（ジャンル定義）の読込・検索サービス"""

from __future__ import annotations

from pathlib import Path

import yaml

from sectorscope.config import THEMES_DIR, UNIVERSE_DIR
from sectorscope.models.universe import UniverseDefinition


def _all_source_dirs() -> list[Path]:
    """走査対象のルートディレクトリ一覧（universe + themes）"""
    dirs = [UNIVERSE_DIR]
    if THEMES_DIR is not None:
        dirs.append(THEMES_DIR)
    return dirs


def load_universe(sector_id: str, market: str = "US") -> UniverseDefinition:
    """指定ジャンルの universe 定義を読み込む

    指定 market → 全 market の順でファイル名・エイリアス・タグを検索する。
    """
    # 1. 指定 market でファイル名一致
    for root in _all_source_dirs():
        yaml_path = root / market.lower() / f"{sector_id}.yaml"
        if yaml_path.exists():
            return _parse_yaml(yaml_path)

    # 2. 全 market でファイル名一致（MIXED 等のフォールバック）
    for root in _all_source_dirs():
        if not root.exists():
            continue
        for market_dir in root.iterdir():
            if not market_dir.is_dir():
                continue
            yaml_path = market_dir / f"{sector_id}.yaml"
            if yaml_path.exists():
                return _parse_yaml(yaml_path)

    # 3. エイリアス・タグで検索（全 market）
    for root in _all_source_dirs():
        if not root.exists():
            continue
        for market_dir in root.iterdir():
            if not market_dir.is_dir():
                continue
            for path in market_dir.glob("*.yaml"):
                defn = _parse_yaml(path)
                if sector_id in defn.aliases or sector_id in defn.tags:
                    return defn

    raise FileNotFoundError(f"Universe '{sector_id}' not found")


def list_universes(market: str | None = None) -> list[UniverseDefinition]:
    """利用可能な全ジャンル・テーマを一覧取得"""
    results: list[UniverseDefinition] = []
    seen_ids: set[str] = set()

    for root in _all_source_dirs():
        if not root.exists():
            continue
        if market:
            markets = [market.lower()]
        else:
            markets = [d.name for d in root.iterdir() if d.is_dir()]

        for m in sorted(markets):
            market_dir = root / m
            if not market_dir.exists():
                continue
            for path in sorted(market_dir.glob("*.yaml")):
                try:
                    defn = _parse_yaml(path)
                    if defn.id not in seen_ids:
                        results.append(defn)
                        seen_ids.add(defn.id)
                except Exception:
                    continue
    return results


def _parse_yaml(path: Path) -> UniverseDefinition:
    """YAML ファイルを UniverseDefinition にパース"""
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return UniverseDefinition(**data)
