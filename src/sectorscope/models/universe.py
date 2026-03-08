"""ジャンル（Universe）定義モデル"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class UniverseDefinition(BaseModel):
    """ジャンル定義ファイルのモデル"""

    id: str
    label: str
    market: Literal["US", "JP", "MIXED"] = "US"
    description: str | None = None
    symbols: list[str]
    aliases: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    names: dict[str, str] = Field(default_factory=dict)
    metadata: dict = Field(default_factory=dict)
    rank_overrides: dict[str, int] = Field(default_factory=dict)
    maintainer: str | None = None
