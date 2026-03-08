"""価格スナップショットモデル"""

from __future__ import annotations

from pydantic import BaseModel


class QuoteSnapshot(BaseModel):
    """銘柄の価格スナップショット"""

    symbol: str
    name: str | None = None
    currency: str | None = None
    exchange: str | None = None
    market_cap: int | None = None
    price: float | None = None
    prev_close: float | None = None
    close_1w_ref: float | None = None
    close_mtd_ref: float | None = None
    close_ytd_ref: float | None = None
    volume: int | None = None
    avg_volume: int | None = None
