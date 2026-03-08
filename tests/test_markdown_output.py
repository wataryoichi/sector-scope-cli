"""Markdown 出力のテスト"""

from sectorscope.formatters.markdown import format_markdown
from sectorscope.models.output import OutputResult, OutputRow


def test_markdown_output_basic():
    result = OutputResult(
        meta={"sector_id": "test"},
        items=[
            OutputRow(
                rank=1,
                symbol="AAPL",
                name="Apple Inc.",
                market_cap=3_000_000_000_000,
                price=180.50,
                pct_1d=1.2,
                pct_1w=-0.5,
                pct_mtd=2.1,
                pct_ytd=15.3,
                volume=50_000_000,
            ),
        ],
    )
    md = format_markdown(result)
    assert "| Rank | Symbol |" in md
    assert "AAPL" in md
    assert "3.0T" in md
    assert "+1.2%" in md
    assert "-0.5%" in md


def test_markdown_output_missing_values():
    result = OutputResult(
        meta={"sector_id": "test"},
        items=[
            OutputRow(rank=1, symbol="MISS"),
        ],
    )
    md = format_markdown(result)
    assert "—" in md


def test_markdown_header_alignment():
    result = OutputResult(meta={}, items=[])
    md = format_markdown(result)
    lines = md.strip().split("\n")
    assert lines[0].startswith("| Rank")
    assert lines[1].startswith("|---:")
