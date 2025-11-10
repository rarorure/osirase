import types

import pytest

from views import view as view_module
from views.view import SendMessageModal


class InteractionResponseStub:
    def __init__(self) -> None:
        self.messages: list[dict[str, object]] = []

    async def send_message(self, content: str, *, ephemeral: bool = False) -> None:
        self.messages.append({"content": content, "ephemeral": ephemeral})


class ClientStub:
    def __init__(self) -> None:
        self.channel_to_return = None
        self.fetch_result = None
        self.fetch_exception: Exception | None = None
        self.fetch_calls = 0

    def get_channel(self, _channel_id: int):  # noqa: D401 - discord 互換シグネチャ
        return self.channel_to_return

    async def fetch_channel(self, _channel_id: int):
        self.fetch_calls += 1
        if self.fetch_exception is not None:
            raise self.fetch_exception
        return self.fetch_result


class InteractionStub:
    def __init__(self, client: ClientStub) -> None:
        self.client = client
        self.response = InteractionResponseStub()


@pytest.mark.asyncio
async def test_process_modal_submission_handles_invalid_channel_id() -> None:
    client = ClientStub()
    interaction = InteractionStub(client)

    await view_module.process_modal_submission(
        interaction,
        channel_id_value="not-an-int",
        message_value="hello",
    )

    assert interaction.response.messages[0]["content"] == SendMessageModal.ERROR_INVALID_ID
    assert interaction.response.messages[0]["ephemeral"] is True


@pytest.mark.asyncio
async def test_process_modal_submission_fetches_channel_when_not_cached(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeMessageable:
        pass

    class FakeChannel(FakeMessageable):
        def __init__(self) -> None:
            self.id = 999
            self.sent: list[str] = []

        async def send(self, content: str) -> None:
            self.sent.append(content)

    monkeypatch.setattr(view_module, "Messageable", FakeMessageable)

    client = ClientStub()
    interaction = InteractionStub(client)
    channel = FakeChannel()
    client.fetch_result = channel

    await view_module.process_modal_submission(
        interaction,
        channel_id_value=str(channel.id),
        message_value="テスト",
    )

    assert client.fetch_calls == 1
    assert channel.sent == ["テスト"]
    assert interaction.response.messages[0]["content"] == SendMessageModal.SUCCESS_MESSAGE.format(channel_id=channel.id)


@pytest.mark.asyncio
async def test_process_modal_submission_handles_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeNotFound(Exception):
        pass

    monkeypatch.setattr(view_module.discord, "NotFound", FakeNotFound, raising=False)

    client = ClientStub()
    interaction = InteractionStub(client)
    client.fetch_exception = FakeNotFound()

    await view_module.process_modal_submission(
        interaction,
        channel_id_value="123",
        message_value="テスト",
    )

    assert interaction.response.messages[0]["content"] == SendMessageModal.ERROR_CHANNEL_NOT_FOUND


@pytest.mark.asyncio
async def test_process_modal_submission_handles_http_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeHTTPException(Exception):
        pass

    monkeypatch.setattr(view_module.discord, "HTTPException", FakeHTTPException, raising=False)

    client = ClientStub()
    interaction = InteractionStub(client)
    client.fetch_exception = FakeHTTPException("boom")

    await view_module.process_modal_submission(
        interaction,
        channel_id_value="123",
        message_value="テスト",
    )

    assert "boom" in interaction.response.messages[0]["content"]


@pytest.mark.asyncio
async def test_process_modal_submission_rejects_non_messageable_channel(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeMessageable:
        pass

    class FakeChannel:
        def __init__(self) -> None:
            self.id = 1

    monkeypatch.setattr(view_module, "Messageable", FakeMessageable)

    client = ClientStub()
    interaction = InteractionStub(client)
    client.channel_to_return = FakeChannel()

    await view_module.process_modal_submission(
        interaction,
        channel_id_value="1",
        message_value="テスト",
    )

    assert interaction.response.messages[0]["content"] == SendMessageModal.ERROR_CHANNEL_NOT_FOUND
