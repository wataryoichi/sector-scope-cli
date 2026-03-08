"""プロバイダ基底クラス"""

from __future__ import annotations

from abc import ABC, abstractmethod

from sectorscope.models.quote import QuoteSnapshot


class PriceProvider(ABC):
    """価格データプロバイダの抽象基底"""

    @abstractmethod
    def fetch_quotes(self, symbols: list[str]) -> list[QuoteSnapshot]:
        """指定シンボルの価格スナップショットを取得"""
        ...
