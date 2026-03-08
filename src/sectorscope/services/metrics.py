"""騰落率計算サービス"""

from __future__ import annotations

from sectorscope.models.output import OutputRow
from sectorscope.models.quote import QuoteSnapshot


def calc_pct(current: float | None, ref: float | None) -> float | None:
    """騰落率を計算: (current / ref - 1) * 100"""
    if current is None or ref is None or ref == 0:
        return None
    return round((current / ref - 1) * 100, 2)


def quote_to_output_row(quote: QuoteSnapshot, rank: int) -> OutputRow:
    """QuoteSnapshot を OutputRow に変換"""
    return OutputRow(
        rank=rank,
        symbol=quote.symbol,
        name=quote.name,
        market_cap=quote.market_cap,
        price=quote.price,
        pct_1d=calc_pct(quote.price, quote.prev_close),
        pct_1w=calc_pct(quote.price, quote.close_1w_ref),
        pct_mtd=calc_pct(quote.price, quote.close_mtd_ref),
        pct_ytd=calc_pct(quote.price, quote.close_ytd_ref),
        volume=quote.volume,
    )
