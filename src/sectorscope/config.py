"""アプリケーション設定"""

from pathlib import Path

from platformdirs import user_cache_dir

# プロジェクトルート
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Universe データディレクトリ
UNIVERSE_DIR = PROJECT_ROOT / "data" / "universe"

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
