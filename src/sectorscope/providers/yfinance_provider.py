"""yfinance を使った価格データプロバイダ"""

from __future__ import annotations

import sys
from collections.abc import Callable
from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf

from sectorscope.config import CACHE_TTL_PRICE
from sectorscope.models.quote import QuoteSnapshot
from sectorscope.providers.base import PriceProvider
from sectorscope.providers.cache import get_cache, set_cache


class YFinanceProvider(PriceProvider):
    """yfinance を使った価格取得"""

    def __init__(self, use_cache: bool = True):
        self._use_cache = use_cache

    def fetch_quotes(
        self,
        symbols: list[str],
        on_progress: Callable[[], None] | None = None,
    ) -> list[QuoteSnapshot]:
        """シンボル群の価格スナップショットを取得"""
        results: list[QuoteSnapshot] = []
        # キャッシュから取得可能なものを先に処理
        to_fetch: list[str] = []
        cached_map: dict[str, QuoteSnapshot] = {}

        if self._use_cache:
            for sym in symbols:
                cached = get_cache(f"quote_{sym}", CACHE_TTL_PRICE)
                if cached:
                    cached_map[sym] = QuoteSnapshot(**cached)
                    if on_progress:
                        on_progress()
                else:
                    to_fetch.append(sym)
        else:
            to_fetch = list(symbols)

        # yfinance でまとめて取得
        if to_fetch:
            fetched = self._fetch_from_yfinance(to_fetch, on_progress=on_progress)
            for q in fetched:
                if self._use_cache:
                    set_cache(f"quote_{q.symbol}", q.model_dump())
                cached_map[q.symbol] = q

        # 元の順序を保持
        for sym in symbols:
            if sym in cached_map:
                results.append(cached_map[sym])
            else:
                results.append(QuoteSnapshot(symbol=sym))

        return results

    def _fetch_from_yfinance(
        self,
        symbols: list[str],
        on_progress: Callable[[], None] | None = None,
    ) -> list[QuoteSnapshot]:
        """yfinance API から価格データを取得"""
        results: list[QuoteSnapshot] = []
        now = datetime.now()
        # 年初来・月初来・週初来の基準日を計算
        year_start = datetime(now.year, 1, 1)
        month_start = datetime(now.year, now.month, 1)
        week_ago = now - timedelta(days=7)
        # 十分な履歴を取得するため年初から
        start_date = year_start - timedelta(days=5)

        try:
            # まとめて履歴取得
            tickers_str = " ".join(symbols)
            hist = yf.download(
                tickers_str,
                start=start_date.strftime("%Y-%m-%d"),
                progress=False,
                group_by="ticker" if len(symbols) > 1 else "column",
                auto_adjust=True,
            )
        except Exception as e:
            print(f"Warning: yfinance download failed: {e}", file=sys.stderr)
            return [QuoteSnapshot(symbol=s) for s in symbols]

        for sym in symbols:
            try:
                quote = self._build_quote(sym, hist, symbols, year_start, month_start, week_ago)
                results.append(quote)
            except Exception:
                results.append(QuoteSnapshot(symbol=sym))
            if on_progress:
                on_progress()

        return results

    def _build_quote(
        self,
        sym: str,
        hist: pd.DataFrame,
        all_symbols: list[str],
        year_start: datetime,
        month_start: datetime,
        week_ago: datetime,
    ) -> QuoteSnapshot:
        """1銘柄分の QuoteSnapshot を構築"""
        if len(all_symbols) == 1:
            sym_hist = hist
        else:
            if sym not in hist.columns.get_level_values(0):
                return QuoteSnapshot(symbol=sym)
            sym_hist = hist[sym]

        sym_hist = sym_hist.dropna(subset=["Close"])
        if sym_hist.empty:
            return QuoteSnapshot(symbol=sym)

        current_price = float(sym_hist["Close"].iloc[-1])
        prev_close = float(sym_hist["Close"].iloc[-2]) if len(sym_hist) >= 2 else None
        volume = int(sym_hist["Volume"].iloc[-1]) if "Volume" in sym_hist.columns else None

        # 基準日 close を取得
        close_ytd = self._get_ref_close(sym_hist, year_start)
        close_mtd = self._get_ref_close(sym_hist, month_start)
        close_1w = self._get_ref_close(sym_hist, week_ago)

        # メタデータ取得
        info = self._get_ticker_info(sym)

        return QuoteSnapshot(
            symbol=sym,
            name=info.get("shortName") or info.get("longName"),
            currency=info.get("currency"),
            exchange=info.get("exchange"),
            market_cap=info.get("marketCap"),
            price=current_price,
            prev_close=prev_close,
            close_1w_ref=close_1w,
            close_mtd_ref=close_mtd,
            close_ytd_ref=close_ytd,
            volume=volume,
            avg_volume=info.get("averageVolume"),
        )

    def _get_ref_close(self, hist: pd.DataFrame, ref_date: datetime) -> float | None:
        """基準日以前の直近営業日終値を取得"""
        ref = pd.Timestamp(ref_date)
        before = hist[hist.index <= ref]
        if before.empty:
            return None
        return float(before["Close"].iloc[-1])

    def _get_ticker_info(self, sym: str) -> dict:
        """メタデータを取得（キャッシュ付き）"""
        from sectorscope.config import CACHE_TTL_METADATA

        if self._use_cache:
            cached = get_cache(f"info_{sym}", CACHE_TTL_METADATA)
            if cached:
                return cached

        try:
            info = yf.Ticker(sym).info or {}
        except Exception:
            info = {}

        if self._use_cache and info:
            set_cache(f"info_{sym}", info)
        return info
