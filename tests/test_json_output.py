"""JSON 出力のテスト"""

import json

from sectorscope.formatters.json_fmt import format_json
from sectorscope.models.output import OutputResult, OutputRow


def test_json_output_valid():
    result = OutputResult(
        meta={"sector_id": "defense", "market": "US"},
        items=[
            OutputRow(rank=1, symbol="LMT", name="Lockheed Martin", market_cap=150_000_000_000),
        ],
    )
    output = format_json(result)
    parsed = json.loads(output)
    assert parsed["meta"]["sector_id"] == "defense"
    assert len(parsed["items"]) == 1
    assert parsed["items"][0]["symbol"] == "LMT"


def test_json_output_with_warnings():
    result = OutputResult(
        meta={},
        items=[],
        warnings=["XYZ: 価格取得失敗"],
    )
    output = format_json(result)
    parsed = json.loads(output)
    assert "warnings" in parsed
    assert len(parsed["warnings"]) == 1


def test_json_output_no_warnings():
    result = OutputResult(meta={}, items=[])
    output = format_json(result)
    parsed = json.loads(output)
    assert "warnings" not in parsed
