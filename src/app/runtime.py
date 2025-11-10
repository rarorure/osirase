from __future__ import annotations

import asyncio
import logging

from .container import build_discord_app
from .config import load_config

LOGGER = logging.getLogger(__name__)


async def run_bot() -> None:
    """設定を読み込み、Discord クライアントを起動する。"""

    try:
        config = load_config()
    except Exception:  # pragma: no cover - 設定エラーは稀
        LOGGER.exception("設定ファイルの読み込みに失敗しました。")
        return

    app = await build_discord_app(config)
    await app.run()


def main() -> None:
    """エントリーポイント。"""

    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_bot())


__all__ = ["main", "run_bot"]
