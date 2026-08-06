import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from websocket.dispatcher import ws_dispatcher


def _app(send_side_effect=None):
    ws_manager = SimpleNamespace(
        send=AsyncMock(side_effect=send_side_effect), disconnect=Mock()
    )
    session_manager = SimpleNamespace(remove=Mock())
    return SimpleNamespace(
        state=SimpleNamespace(
            event_queue=asyncio.Queue(),
            ws_manager=ws_manager,
            session_manager=session_manager,
        )
    )


async def _run_dispatcher_briefly(app):
    task = asyncio.create_task(ws_dispatcher(app))
    await asyncio.sleep(0.02)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


@pytest.mark.asyncio
async def test_ws_dispatcher_forwards_event_to_ws_manager():
    app = _app()
    await app.state.event_queue.put({"client_id": "client-1", "data": {"tick": 1}})

    await _run_dispatcher_briefly(app)

    app.state.ws_manager.send.assert_awaited_once_with("client-1", {"tick": 1})


@pytest.mark.asyncio
async def test_ws_dispatcher_disconnects_client_on_send_failure():
    app = _app(send_side_effect=RuntimeError("boom"))
    await app.state.event_queue.put({"client_id": "client-1", "data": {"tick": 1}})

    await _run_dispatcher_briefly(app)

    app.state.ws_manager.disconnect.assert_called_once_with("client-1")
    app.state.session_manager.remove.assert_called_once_with("client-1")
