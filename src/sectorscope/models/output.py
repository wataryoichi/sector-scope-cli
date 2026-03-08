"""出力データモデル"""

from __future__ import annotations

from pydantic import BaseModel


class OutputRow(BaseModel):
    """表示用の1行データ"""

    rank: int
    symbol: str
    name: str | None = None
    market_cap: int | None = None
    price: float | None = None
    pct_1d: float | None = None
    pct_1w: float | None = None
    pct_mtd: float | None = None
    pct_ytd: float | None = None
    volume: int | None = None


class OutputResult(BaseModel):
    """コマンド出力全体"""

    meta: dict
    items: list[OutputRow]
    warnings: list[str] = []
