"""アプリケーション設定"""

from pathlib import Path

from platformdirs import user_cache_dir, user_config_dir

# パッケージ同梱の Universe データ（フォールバック）
_PACKAGE_UNIVERSE_DIR = Path(__file__).resolve().parent / "data_universe"

# ユーザー設定ディレクトリ（~/.config/sectorscope/universe/）
_USER_UNIVERSE_DIR = Path(user_config_dir("sectorscope")) / "universe"

# 開発用: プロジェクトルートの data/universe/
_DEV_UNIVERSE_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "universe"


def _resolve_universe_dir() -> Path:
    """Universe ディレクトリを優先順に解決:
    1. ユーザー設定 (~/.config/sectorscope/universe/)
    2. 開発用 (プロジェクトルート data/universe/) — YAML が存在する場合のみ
    3. パッケージ同梱 (src/sectorscope/data_universe/)
    """
    if _USER_UNIVERSE_DIR.exists() and any(_USER_UNIVERSE_DIR.rglob("*.yaml")):
        return _USER_UNIVERSE_DIR
    if _DEV_UNIVERSE_DIR.exists() and any(_DEV_UNIVERSE_DIR.rglob("*.yaml")):
        return _DEV_UNIVERSE_DIR
    return _PACKAGE_UNIVERSE_DIR


# Universe データディレクトリ
UNIVERSE_DIR = _resolve_universe_dir()

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
