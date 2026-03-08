"""ソートサービス"""

from __future__ import annotations

from sectorscope.models.output import OutputRow

SORT_KEY_MAP: dict[str, str] = {
    "market_cap": "market_cap",
    "price": "price",
    "1d": "pct_1d",
    "1w": "pct_1w",
    "mtd": "pct_mtd",
    "ytd": "pct_ytd",
    "volume": "volume",
    "symbol": "symbol",
    "name": "name",
}


def sort_rows(
    rows: list[OutputRow],
    sort_by: str = "market_cap",
    descending: bool = True,
    rank_overrides: dict[str, int] | None = None,
) -> list[OutputRow]:
    """OutputRow のリストをソートし、rank を振り直す"""
    if sort_by == "custom" and rank_overrides:
        sorted_rows = sorted(
            rows,
            key=lambda r: rank_overrides.get(r.symbol, 9999),
        )
    else:
        attr = SORT_KEY_MAP.get(sort_by, "market_cap")
        sorted_rows = sorted(
            rows,
            key=lambda r: _sort_key(getattr(r, attr, None), r.symbol, descending),
        )
        if descending:
            # None 以外を逆順、None は末尾維持
            has_val = [r for r in sorted_rows if getattr(r, attr, None) is not None]
            no_val = [r for r in sorted_rows if getattr(r, attr, None) is None]
            has_val.reverse()
            sorted_rows = has_val + no_val

    for i, row in enumerate(sorted_rows, start=1):
        row.rank = i
    return sorted_rows


def _sort_key(val: object, symbol: str, descending: bool) -> tuple[int, float | str, str]:
    """None を常に末尾に送るソートキー"""
    if val is None:
        return (1, 0, symbol)
    if isinstance(val, str):
        return (0, val.lower(), symbol)
    return (0, float(val), symbol)
