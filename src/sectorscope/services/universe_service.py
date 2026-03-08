"""Universe（ジャンル定義）の読込・検索サービス"""

from __future__ import annotations

from pathlib import Path

import yaml

from sectorscope.config import UNIVERSE_DIR
from sectorscope.models.universe import UniverseDefinition


def load_universe(sector_id: str, market: str = "US") -> UniverseDefinition:
    """指定ジャンルの universe 定義を読み込む"""
    market_dir = UNIVERSE_DIR / market.lower()
    yaml_path = market_dir / f"{sector_id}.yaml"
    if not yaml_path.exists():
        # エイリアスで検索
        for path in market_dir.glob("*.yaml"):
            defn = _parse_yaml(path)
            if sector_id in defn.aliases or sector_id in defn.tags:
                return defn
        raise FileNotFoundError(f"Universe '{sector_id}' not found in market '{market}'")
    return _parse_yaml(yaml_path)


def list_universes(market: str | None = None) -> list[UniverseDefinition]:
    """利用可能な全ジャンルを一覧取得"""
    results: list[UniverseDefinition] = []
    if market:
        markets = [market.lower()]
    else:
        markets = [d.name for d in UNIVERSE_DIR.iterdir() if d.is_dir()]

    for m in sorted(markets):
        market_dir = UNIVERSE_DIR / m
        if not market_dir.exists():
            continue
        for path in sorted(market_dir.glob("*.yaml")):
            try:
                results.append(_parse_yaml(path))
            except Exception:
                continue
    return results


def _parse_yaml(path: Path) -> UniverseDefinition:
    """YAML ファイルを UniverseDefinition にパース"""
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return UniverseDefinition(**data)
