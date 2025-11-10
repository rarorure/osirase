from __future__ import annotations

import logging
from dataclasses import dataclass

from app.config import AppConfig
from bot import BotClient, register_commands

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class DiscordApplication:
    """Discord クライアントとトークンをまとめた実行ラッパー。"""

    client: BotClient
    token: str

    async def run(self) -> None:
        """クライアントを起動する。"""

        async with self.client:
            await self.client.start(self.token)


async def build_discord_app(config: AppConfig) -> DiscordApplication:
    """Discord クライアントを初期化し、コマンド登録までを完了させる。"""

    client = BotClient()
    await register_commands(client)
    LOGGER.info("Discord クライアントの初期化が完了し、コマンドを登録しました。")
    return DiscordApplication(client=client, token=config.discord.token)


__all__ = ["DiscordApplication", "build_discord_app"]
