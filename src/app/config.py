from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class DiscordSettings:
    """Discord Bot に必要な設定値を保持する。"""

    token: str


@dataclass(frozen=True, slots=True)
class AppConfig:
    """アプリケーション全体の設定値をまとめる。"""

    discord: DiscordSettings


def _load_env_file(env_file: str | Path | None) -> None:
    """`.env` ファイルを読み込む。"""

    if env_file is None:
        load_dotenv()
        return

    path = Path(env_file)
    if path.is_file():
        load_dotenv(dotenv_path=path)
        return

    raise FileNotFoundError(f".env file not found at: {path}")


def _prepare_client_token(raw_token: str | None) -> str:
    """Discord Bot トークンを検証して整形する。"""

    if raw_token is None or raw_token.strip() == "":
        raise ValueError("Discord bot token is not set in environment variables.")
    return raw_token.strip()


def load_config(env_file: str | Path | None = None) -> AppConfig:
    """環境変数と .env から設定を読み込む。"""

    _load_env_file(env_file)

    token = _prepare_client_token(raw_token=os.getenv("DISCORD_BOT_TOKEN"))

    LOGGER.info("設定の読み込みが完了しました。")

    return AppConfig(
        discord=DiscordSettings(token=token),
    )


__all__ = ["AppConfig", "DiscordSettings", "load_config"]
