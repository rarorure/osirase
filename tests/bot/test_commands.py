import types

import pytest

from bot import register_commands
from views import SendModalView


class FakeResponse:
    def __init__(self) -> None:
        self.deferred_ephemeral: bool | None = None

    async def defer(self, *, ephemeral: bool = False) -> None:
        self.deferred_ephemeral = ephemeral


class FakeFollowup:
    def __init__(self) -> None:
        self.sent: list[dict[str, object]] = []

    async def send(self, content: str, *, view=None, ephemeral: bool = False) -> None:
        self.sent.append({"content": content, "view": view, "ephemeral": ephemeral})


class FakeInteraction:
    def __init__(self) -> None:
        self.user = "tester"
        self.response = FakeResponse()
        self.followup = FakeFollowup()


class FakeCommandTree:
    def __init__(self) -> None:
        self.registered: dict[str, dict[str, object]] = {}

    def command(self, *, name: str, description: str):  # noqa: D401 - discord 互換API
        def decorator(func):
            self.registered[name] = {"callback": func, "description": description}
            return func

        return decorator


@pytest.mark.asyncio
async def test_register_commands_registers_setup_and_sends_view() -> None:
    tree = FakeCommandTree()
    client = types.SimpleNamespace(tree=tree)

    await register_commands(client)
    assert "setup" in tree.registered

    interaction = FakeInteraction()
    await tree.registered["setup"]["callback"](interaction)

    assert interaction.response.deferred_ephemeral is True
    assert interaction.followup.sent[0]["ephemeral"] is True
    assert isinstance(interaction.followup.sent[0]["view"], SendModalView)
