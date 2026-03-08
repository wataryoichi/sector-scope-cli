"""アプリケーション設定"""

from pathlib import Path

from platformdirs import user_cache_dir

# パッケージ同梱の Universe データ（フォールバック）
_PACKAGE_UNIVERSE_DIR = Path(__file__).resolve().parent / "data_universe"
_PACKAGE_THEMES_DIR = Path(__file__).resolve().parent / "data_themes"

# ユーザーカスタムディレクトリ（~/.sectorscope/）
_USER_UNIVERSE_DIR = Path.home() / ".sectorscope" / "universe"
_USER_THEMES_DIR = Path.home() / ".sectorscope" / "themes"

# 開発用: プロジェクトルートの data/
_DEV_UNIVERSE_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "universe"
_DEV_THEMES_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "themes"


def _resolve_universe_dir() -> Path:
    """Universe ディレクトリを優先順に解決:
    1. ユーザーカスタム (~/.sectorscope/universe/)
    2. 開発用 (プロジェクトルート data/universe/) — YAML が存在する場合のみ
    3. パッケージ同梱 (src/sectorscope/data_universe/)
    """
    if _USER_UNIVERSE_DIR.exists() and any(_USER_UNIVERSE_DIR.rglob("*.yaml")):
        return _USER_UNIVERSE_DIR
    if _DEV_UNIVERSE_DIR.exists() and any(_DEV_UNIVERSE_DIR.rglob("*.yaml")):
        return _DEV_UNIVERSE_DIR
    return _PACKAGE_UNIVERSE_DIR


def _resolve_themes_dir() -> Path | None:
    """Themes ディレクトリを優先順に解決（存在しなければ None）:
    1. ユーザーカスタム (~/.sectorscope/themes/)
    2. 開発用 (プロジェクトルート data/themes/)
    3. パッケージ同梱 (src/sectorscope/data_themes/)
    """
    if _USER_THEMES_DIR.exists() and any(_USER_THEMES_DIR.rglob("*.yaml")):
        return _USER_THEMES_DIR
    if _DEV_THEMES_DIR.exists() and any(_DEV_THEMES_DIR.rglob("*.yaml")):
        return _DEV_THEMES_DIR
    if _PACKAGE_THEMES_DIR.exists() and any(_PACKAGE_THEMES_DIR.rglob("*.yaml")):
        return _PACKAGE_THEMES_DIR
    return None


# Universe データディレクトリ
UNIVERSE_DIR = _resolve_universe_dir()

# Themes データディレクトリ（揺れやすいテーマ定義用）
THEMES_DIR = _resolve_themes_dir()

# キャッシュディレクトリ
CACHE_DIR = Path(user_cache_dir("sectorscope"))

# キャッシュ TTL (秒)
CACHE_TTL_METADATA = 7 * 24 * 3600  # 7日
CACHE_TTL_PRICE = 15 * 60  # 15分
CACHE_TTL_HISTORY = 24 * 3600  # 1日

# デフォルト設定
DEFAULT_MARKET = "US"
DEFAULT_SORT = "market_cap"
DEFAULT_FORMAT = "table"
DEFAULT_ORDER = "desc"
