"""ファイルベースのキャッシュ"""

from __future__ import annotations

import json
import time
from pathlib import Path

from sectorscope.config import CACHE_DIR


def get_cache(key: str, ttl: int) -> dict | None:
    """キャッシュからデータを取得。TTL超過なら None"""
    path = _cache_path(key)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if time.time() - data.get("_ts", 0) > ttl:
            return None
        return data.get("payload")
    except (json.JSONDecodeError, KeyError):
        return None


def set_cache(key: str, payload: dict | list) -> None:
    """データをキャッシュに保存"""
    path = _cache_path(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {"_ts": time.time(), "payload": payload}
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def _cache_path(key: str) -> Path:
    """キャッシュファイルのパスを生成"""
    safe_key = key.replace("/", "_").replace("\\", "_")
    return CACHE_DIR / f"{safe_key}.json"
