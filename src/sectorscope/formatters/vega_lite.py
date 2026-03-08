"""Vega-Lite JSON 出力フォーマッタ"""

from __future__ import annotations

import json

from sectorscope.models.output import OutputResult


def format_vega_lite(
    result: OutputResult,
    metric: str = "pct_ytd",
    wrap_codeblock: bool = False,
) -> str:
    """Vega-Lite JSON を生成

    Args:
        result: 出力データ
        metric: 使用する指標フィールド名 (pct_1d, pct_1w, pct_mtd, pct_ytd)
        wrap_codeblock: True なら ```vega-lite ... ``` で囲む
    """
    metric_label = _metric_label(metric)

    values = []
    for row in result.items:
        val = getattr(row, metric, None)
        if val is not None:
            values.append({
                "symbol": row.symbol,
                "name": row.name or row.symbol,
                metric: val,
            })

    spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "title": f"{result.meta.get('sector_label', result.meta.get('sector_id', ''))} - {metric_label}",
        "data": {"values": values},
        "mark": "bar",
        "encoding": {
            "y": {"field": "symbol", "type": "nominal", "sort": "-x", "title": "Symbol"},
            "x": {"field": metric, "type": "quantitative", "title": metric_label},
            "color": {
                "condition": {"test": f"datum.{metric} >= 0", "value": "#22c55e"},
                "value": "#ef4444",
            },
            "tooltip": [
                {"field": "symbol", "type": "nominal"},
                {"field": "name", "type": "nominal"},
                {"field": metric, "type": "quantitative", "format": ".1f"},
            ],
        },
    }

    json_str = json.dumps(spec, ensure_ascii=False, indent=2)

    if wrap_codeblock:
        return f"```vega-lite\n{json_str}\n```"
    return json_str


def _metric_label(metric: str) -> str:
    labels = {
        "pct_1d": "1D Change (%)",
        "pct_1w": "1W Change (%)",
        "pct_mtd": "MTD Change (%)",
        "pct_ytd": "YTD Change (%)",
    }
    return labels.get(metric, metric)
