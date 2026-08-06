from unittest.mock import AsyncMock

import pytest

from websocket.manager import WSManager


class _FakeWebSocket:  # pylint: disable=too-few-public-methods
    def __init__(self, send_json_side_effect=None):
        self.accept = AsyncMock()
        self.send_json = AsyncMock(side_effect=send_json_side_effect)


@pytest.mark.asyncio
async def test_connect_accepts_and_registers_client():
    manager = WSManager()
    ws = _FakeWebSocket()

    await manager.connect(ws, "client-1")

    ws.accept.assert_awaited_once()
    assert manager.clients["client-1"] is ws


def test_disconnect_removes_registered_client():
    manager = WSManager()
    manager.clients["client-1"] = _FakeWebSocket()

    manager.disconnect("client-1")

    assert "client-1" not in manager.clients


def test_disconnect_is_noop_when_client_unknown():
    manager = WSManager()

    manager.disconnect("unknown-client")

    assert not manager.clients


@pytest.mark.asyncio
async def test_send_forwards_data_to_registered_client():
    manager = WSManager()
    ws = _FakeWebSocket()
    manager.clients["client-1"] = ws

    await manager.send("client-1", {"tick": 1})

    ws.send_json.assert_awaited_once_with({"tick": 1})


@pytest.mark.asyncio
async def test_send_is_noop_when_client_unknown():
    manager = WSManager()

    await manager.send("unknown-client", {"tick": 1})


@pytest.mark.asyncio
async def test_send_disconnects_client_when_send_fails():
    manager = WSManager()
    ws = _FakeWebSocket(send_json_side_effect=RuntimeError("boom"))
    manager.clients["client-1"] = ws

    await manager.send("client-1", {"tick": 1})

    assert "client-1" not in manager.clients
