"""騰落率計算のテスト"""

from sectorscope.models.quote import QuoteSnapshot
from sectorscope.services.metrics import calc_pct, quote_to_output_row


def test_calc_pct_positive():
    assert calc_pct(110.0, 100.0) == 10.0


def test_calc_pct_negative():
    assert calc_pct(90.0, 100.0) == -10.0


def test_calc_pct_zero_ref():
    assert calc_pct(100.0, 0) is None


def test_calc_pct_none_current():
    assert calc_pct(None, 100.0) is None


def test_calc_pct_none_ref():
    assert calc_pct(100.0, None) is None


def test_quote_to_output_row():
    q = QuoteSnapshot(
        symbol="TEST",
        name="Test Corp",
        market_cap=1_000_000_000,
        price=110.0,
        prev_close=100.0,
        close_1w_ref=105.0,
        close_mtd_ref=108.0,
        close_ytd_ref=90.0,
        volume=500000,
    )
    row = quote_to_output_row(q, rank=1)
    assert row.symbol == "TEST"
    assert row.pct_1d == 10.0
    assert row.pct_1w == pytest.approx(4.76, abs=0.01)
    assert row.pct_ytd == pytest.approx(22.22, abs=0.01)


def test_quote_to_output_row_missing_data():
    q = QuoteSnapshot(symbol="EMPTY")
    row = quote_to_output_row(q, rank=1)
    assert row.pct_1d is None
    assert row.pct_1w is None
    assert row.pct_ytd is None
    assert row.market_cap is None


import pytest
