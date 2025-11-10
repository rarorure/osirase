from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import discord

from views import SendModalView

if TYPE_CHECKING:
    from bot.client import BotClient

LOGGER = logging.getLogger(__name__)


async def register_commands(client: "BotClient") -> None:
    """クライアントのアプリケーションコマンドを登録する。"""

    tree = client.tree

    @tree.command(name="setup", description="メッセージ送信のセットアップを行います。")
    async def command_setup(interaction: discord.Interaction) -> None:  # pragma: no cover - Discord 実行時にテスト
        LOGGER.info("/setup コマンドを実行したユーザー: %s", interaction.user)
        await interaction.response.defer(ephemeral=True)
        view = SendModalView()
        await interaction.followup.send(
            "📨 下のボタンからメッセージ送信モーダルを開けます。",
            view=view,
            ephemeral=True,
        )


__all__ = ["register_commands"]
