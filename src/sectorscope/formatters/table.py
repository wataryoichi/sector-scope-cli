"""Rich テーブル出力フォーマッタ"""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

from sectorscope.models.output import OutputResult


def format_table(result: OutputResult, console: Console | None = None) -> None:
    """Rich テーブルで出力"""
    if console is None:
        console = Console()

    meta = result.meta
    title = f"{meta.get('sector_label', meta.get('sector_id', ''))} ({meta.get('market', 'US')})"

    table = Table(title=title, show_lines=False)
    table.add_column("#", justify="right", style="dim")
    table.add_column("Symbol", style="bold cyan")
    table.add_column("Name")
    table.add_column("Market Cap", justify="right")
    table.add_column("Price", justify="right")
    table.add_column("1D", justify="right")
    table.add_column("1W", justify="right")
    table.add_column("MTD", justify="right")
    table.add_column("YTD", justify="right")
    table.add_column("Volume", justify="right")

    for row in result.items:
        table.add_row(
            str(row.rank),
            row.symbol,
            row.name or "—",
            _fmt_cap(row.market_cap),
            _fmt_price(row.price),
            _fmt_pct(row.pct_1d),
            _fmt_pct(row.pct_1w),
            _fmt_pct(row.pct_mtd),
            _fmt_pct(row.pct_ytd),
            _fmt_vol(row.volume),
        )

    console.print(table)

    for w in result.warnings:
        console.print(f"[yellow]Warning: {w}[/yellow]")


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
    color = "green" if val >= 0 else "red"
    return f"[{color}]{val:+.1f}%[/{color}]"


def _fmt_vol(val: int | None) -> str:
    if val is None:
        return "—"
    if val >= 1_000_000:
        return f"{val / 1_000_000:.1f}M"
    if val >= 1_000:
        return f"{val / 1_000:.1f}K"
    return f"{val:,}"
