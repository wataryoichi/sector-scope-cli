"""SectorScope CLI メインエントリポイント"""

from __future__ import annotations

from enum import Enum
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from sectorscope import __version__

app = typer.Typer(
    name="sectorscope",
    help="テーマ・セクター単位で株式の騰落率を確認するCLIツール",
    no_args_is_help=True,
)
universe_app = typer.Typer(help="Universe（セクター定義）管理コマンド")
app.add_typer(universe_app, name="universe")

console = Console()


class OutputFormat(str, Enum):
    table = "table"
    markdown = "markdown"
    json = "json"
    vega_lite = "vega-lite"


class SortKey(str, Enum):
    market_cap = "market_cap"
    price = "price"
    d1 = "1d"
    w1 = "1w"
    mtd = "mtd"
    ytd = "ytd"
    volume = "volume"
    symbol = "symbol"
    name = "name"
    custom = "custom"


def version_callback(value: bool) -> None:
    if value:
        console.print(f"sectorscope {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option("--version", "-v", callback=version_callback, is_eager=True, help="バージョン表示"),
    ] = None,
) -> None:
    """SectorScope CLI"""


@app.command(name="list-sectors")
def list_sectors(
    market: Annotated[Optional[str], typer.Option("--market", "-m", help="対象市場 (us/jp)")] = None,
    fmt: Annotated[OutputFormat, typer.Option("--format", "-f", help="出力形式")] = OutputFormat.table,
) -> None:
    """利用可能なセクター一覧を表示"""
    from sectorscope.services.universe_service import list_universes

    universes = list_universes(market=market)
    if not universes:
        console.print("[yellow]セクター定義が見つかりません。data/universe/ にYAMLファイルを配置してください。[/yellow]")
        raise typer.Exit(1)

    if fmt == OutputFormat.json:
        import json

        items = [
            {
                "id": u.id,
                "label": u.label,
                "market": u.market,
                "symbol_count": len(u.symbols),
                "description": u.description,
                "updated_at": u.metadata.get("updated_at"),
            }
            for u in universes
        ]
        print(json.dumps(items, ensure_ascii=False, indent=2))
        return

    if fmt == OutputFormat.markdown:
        lines = [
            "| ID | Label | Market | Symbols | Description |",
            "|---|---|---|---:|---|",
        ]
        for u in universes:
            lines.append(
                f"| {u.id} | {u.label} | {u.market} | {len(u.symbols)} | {u.description or '—'} |"
            )
        console.print("\n".join(lines))
        return

    # table 形式
    table = Table(title="Sectors / Themes")
    table.add_column("ID", style="bold cyan")
    table.add_column("Label")
    table.add_column("Market")
    table.add_column("Symbols", justify="right")
    table.add_column("Description")

    for u in universes:
        table.add_row(u.id, u.label, u.market, str(len(u.symbols)), u.description or "—")

    console.print(table)


@app.command()
def show(
    sector_id: Annotated[str, typer.Argument(help="セクターID")],
    market: Annotated[Optional[str], typer.Option("--market", "-m", help="対象市場")] = None,
    sort: Annotated[SortKey, typer.Option("--sort", "-s", help="ソートキー")] = SortKey.market_cap,
    desc: Annotated[bool, typer.Option("--desc", help="降順")] = True,
    asc: Annotated[bool, typer.Option("--asc", help="昇順")] = False,
    fmt: Annotated[OutputFormat, typer.Option("--format", "-f", help="出力形式")] = OutputFormat.table,
    limit: Annotated[Optional[int], typer.Option("--limit", "-l", help="表示件数制限")] = None,
    no_cache: Annotated[bool, typer.Option("--no-cache", help="キャッシュ無効")] = False,
    metric: Annotated[str, typer.Option("--metric", help="vega-lite 用指標 (pct_1d/pct_1w/pct_mtd/pct_ytd)")] = "pct_ytd",
    wrap_code: Annotated[bool, typer.Option("--wrap-code", help="vega-lite を ```vega-lite で囲む")] = False,
    output: Annotated[Optional[str], typer.Option("--output", "-o", help="出力先ファイルパス")] = None,
) -> None:
    """指定セクターの銘柄一覧と騰落率を表示"""
    from sectorscope.formatters.json_fmt import format_json
    from sectorscope.formatters.markdown import format_markdown
    from sectorscope.formatters.table import format_table
    from sectorscope.formatters.vega_lite import format_vega_lite
    from sectorscope.models.output import OutputResult
    from sectorscope.providers.yfinance_provider import YFinanceProvider
    from sectorscope.services.metrics import quote_to_output_row
    from sectorscope.services.sorting import sort_rows
    from sectorscope.services.universe_service import load_universe

    effective_market = (market or "US").upper()
    descending = not asc  # --asc が指定されたら昇順

    try:
        universe = load_universe(sector_id, market=effective_market)
    except FileNotFoundError:
        console.print(f"[red]セクター '{sector_id}' が見つかりません。[/red]")
        raise typer.Exit(1)

    provider = YFinanceProvider(use_cache=not no_cache)

    from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total} 銘柄"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(
            f"{universe.label} の価格データを取得中",
            total=len(universe.symbols),
        )
        quotes = provider.fetch_quotes(
            universe.symbols,
            on_progress=lambda: progress.advance(task),
        )

    # YAML の names をフォールバック名として適用
    yaml_names = universe.names or {}
    for q in quotes:
        if not q.name and q.symbol in yaml_names:
            q.name = yaml_names[q.symbol]

    warnings: list[str] = []
    rows = []
    for i, q in enumerate(quotes, start=1):
        if q.price is None:
            warnings.append(f"{q.symbol}: 価格取得失敗")
        rows.append(quote_to_output_row(q, rank=i))

    sorted_rows = sort_rows(
        rows,
        sort_by=sort.value,
        descending=descending,
        rank_overrides=universe.rank_overrides or None,
    )

    if limit:
        sorted_rows = sorted_rows[:limit]
        for i, row in enumerate(sorted_rows, start=1):
            row.rank = i

    result = OutputResult(
        meta={
            "tool": "sectorscope",
            "market": effective_market,
            "sector_id": universe.id,
            "sector_label": universe.label,
            "sort": sort.value,
            "order": "desc" if descending else "asc",
        },
        items=sorted_rows,
        warnings=warnings,
    )

    # 出力生成
    output_text: str | None = None
    if fmt == OutputFormat.json:
        output_text = format_json(result)
    elif fmt == OutputFormat.markdown:
        output_text = format_markdown(result)
    elif fmt == OutputFormat.vega_lite:
        output_text = format_vega_lite(result, metric=metric, wrap_codeblock=wrap_code)

    # ファイル出力
    if output:
        from pathlib import Path
        text = output_text if output_text else format_markdown(result)
        Path(output).write_text(text, encoding="utf-8")
        console.print(f"[green]出力を {output} に保存しました。[/green]")
        return

    # コンソール出力
    if output_text:
        print(output_text)
    else:
        format_table(result, console=console)


@universe_app.command()
def validate() -> None:
    """セクター定義ファイルを検証"""
    from sectorscope.services.universe_service import list_universes

    universes = list_universes()
    errors: list[str] = []

    all_symbols: dict[str, list[str]] = {}
    all_aliases: dict[str, list[str]] = {}

    for u in universes:
        # 空シンボル
        if not u.symbols:
            errors.append(f"[{u.id}] symbols が空です")

        # シンボル重複（セクター内）
        seen = set()
        for s in u.symbols:
            if s in seen:
                errors.append(f"[{u.id}] symbol '{s}' が重複しています")
            seen.add(s)

        # market 検証
        if u.market not in ("US", "JP", "MIXED"):
            errors.append(f"[{u.id}] 不正な market: '{u.market}'")

        # 全セクター横断の重複チェック用
        for s in u.symbols:
            all_symbols.setdefault(s, []).append(u.id)
        for a in u.aliases:
            all_aliases.setdefault(a, []).append(u.id)

    # エイリアス重複チェック
    for alias, ids in all_aliases.items():
        if len(ids) > 1:
            errors.append(f"alias '{alias}' が複数セクターで使用: {', '.join(ids)}")

    if errors:
        console.print("[red]検証エラー:[/red]")
        for e in errors:
            console.print(f"  - {e}")
        raise typer.Exit(1)
    else:
        console.print(f"[green]全 {len(universes)} セクターの検証に成功しました。[/green]")
