"""Markdown テーブル出力フォーマッタ"""

from __future__ import annotations

from sectorscope.models.output import OutputResult


def format_markdown(result: OutputResult) -> str:
    """Markdown テーブル文字列を生成"""
    lines: list[str] = []

    # ヘッダ
    lines.append("| Rank | Symbol | Name | Market Cap | Price | 1D | 1W | MTD | YTD | Volume |")
    lines.append("|---:|---|---|---:|---:|---:|---:|---:|---:|---:|")

    for row in result.items:
        lines.append(
            f"| {row.rank} "
            f"| {row.symbol} "
            f"| {row.name or '—'} "
            f"| {_fmt_cap(row.market_cap)} "
            f"| {_fmt_price(row.price)} "
            f"| {_fmt_pct(row.pct_1d)} "
            f"| {_fmt_pct(row.pct_1w)} "
            f"| {_fmt_pct(row.pct_mtd)} "
            f"| {_fmt_pct(row.pct_ytd)} "
            f"| {_fmt_vol(row.volume)} |"
        )

    return "\n".join(lines)


def _fmt_cap(val: int | None) -> str:
    if val is None:
        return "—"
    if val >= 1_000_000_000_000:
        return f"{val / 1_000_000_000_000:.1f}T"
    if val >= 1_000_000_000:
        return f"{val / 1_000_000_000:.1f}B"
    if val >= 1_000_000:
        return f"{val / 1_000_000:.1f}M"
    return f"{val:,}"


def _fmt_price(val: float | None) -> str:
    if val is None:
        return "—"
    return f"{val:,.2f}"


def _fmt_pct(val: float | None) -> str:
    if val is None:
        return "—"
    return f"{val:+.1f}%"


def _fmt_vol(val: int | None) -> str:
    if val is None:
        return "—"
    if val >= 1_000_000:
        return f"{val / 1_000_000:.1f}M"
    if val >= 1_000:
        return f"{val / 1_000:.1f}K"
    return f"{val:,}"
