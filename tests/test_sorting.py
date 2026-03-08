"""ソートのテスト"""

from sectorscope.models.output import OutputRow
from sectorscope.services.sorting import sort_rows


def _make_rows():
    return [
        OutputRow(rank=1, symbol="AAA", market_cap=100, pct_ytd=5.0),
        OutputRow(rank=2, symbol="BBB", market_cap=300, pct_ytd=-2.0),
        OutputRow(rank=3, symbol="CCC", market_cap=200, pct_ytd=10.0),
    ]


def test_sort_by_market_cap_desc():
    rows = sort_rows(_make_rows(), sort_by="market_cap", descending=True)
    assert [r.symbol for r in rows] == ["BBB", "CCC", "AAA"]
    assert rows[0].rank == 1


def test_sort_by_market_cap_asc():
    rows = sort_rows(_make_rows(), sort_by="market_cap", descending=False)
    assert [r.symbol for r in rows] == ["AAA", "CCC", "BBB"]


def test_sort_by_ytd():
    rows = sort_rows(_make_rows(), sort_by="ytd", descending=True)
    assert [r.symbol for r in rows] == ["CCC", "AAA", "BBB"]


def test_sort_by_symbol():
    rows = sort_rows(_make_rows(), sort_by="symbol", descending=False)
    assert [r.symbol for r in rows] == ["AAA", "BBB", "CCC"]


def test_sort_with_none_values():
    rows = [
        OutputRow(rank=1, symbol="AAA", market_cap=100),
        OutputRow(rank=2, symbol="BBB", market_cap=None),
        OutputRow(rank=3, symbol="CCC", market_cap=200),
    ]
    sorted_rows = sort_rows(rows, sort_by="market_cap", descending=True)
    # None は末尾
    assert sorted_rows[-1].symbol == "BBB"


def test_sort_custom():
    rows = _make_rows()
    overrides = {"CCC": 1, "AAA": 2, "BBB": 3}
    sorted_rows = sort_rows(rows, sort_by="custom", rank_overrides=overrides)
    assert [r.symbol for r in sorted_rows] == ["CCC", "AAA", "BBB"]
