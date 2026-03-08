"""JSON 出力フォーマッタ"""

from __future__ import annotations

import json

from sectorscope.models.output import OutputResult


def format_json(result: OutputResult) -> str:
    """JSON 文字列を生成"""
    output = {
        "meta": result.meta,
        "items": [row.model_dump() for row in result.items],
    }
    if result.warnings:
        output["warnings"] = result.warnings
    return json.dumps(output, ensure_ascii=False, indent=2)
