from __future__ import annotations

import logging

import discord

LOGGER = logging.getLogger(__name__)


class BotClient(discord.Client):
    """Discord Client 拡張。コマンド登録と同期を担当する。"""

    def __init__(self, *, intents: discord.Intents | None = None) -> None:
        super().__init__(intents=intents or discord.Intents.all())
        self.tree = discord.app_commands.CommandTree(self)

    async def on_ready(self) -> None:
        if self.user is None:
            LOGGER.warning("クライアントユーザー情報を取得できませんでした。")
            return

        LOGGER.info("ログイン完了: %s (ID: %s)", self.user, self.user.id)
        await self.tree.sync()
        LOGGER.info("アプリケーションコマンドの同期が完了しました。")
        LOGGER.info("準備完了。")


__all__ = ["BotClient"]
