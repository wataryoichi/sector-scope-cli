"""Universe 読込のテスト"""

import tempfile
from pathlib import Path

import pytest
import yaml

from sectorscope.models.universe import UniverseDefinition
from sectorscope.services.universe_service import _parse_yaml, list_universes


def test_parse_yaml(tmp_path):
    data = {
        "id": "test-sector",
        "label": "Test Sector",
        "market": "US",
        "description": "A test sector",
        "symbols": ["AAPL", "MSFT"],
        "aliases": ["test"],
        "tags": ["test"],
    }
    yaml_path = tmp_path / "test.yaml"
    yaml_path.write_text(yaml.dump(data))

    result = _parse_yaml(yaml_path)
    assert isinstance(result, UniverseDefinition)
    assert result.id == "test-sector"
    assert result.symbols == ["AAPL", "MSFT"]
    assert result.market == "US"


def test_list_universes_returns_real_data():
    """実際の data/universe/ からロードできることを確認"""
    universes = list_universes(market="us")
    assert len(universes) > 0
    assert all(isinstance(u, UniverseDefinition) for u in universes)


def test_universe_definition_defaults():
    u = UniverseDefinition(id="x", label="X", symbols=["A"])
    assert u.market == "US"
    assert u.aliases == []
    assert u.tags == []
    assert u.rank_overrides == {}
