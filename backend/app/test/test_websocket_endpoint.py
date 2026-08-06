from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastapi import WebSocketDisconnect

from engine.controller import Controller
from websocket.endpoint import (
    _handle_grid_size,
    _handle_next_step,
    _handle_reset,
    _handle_set_rules,
    _handle_set_speed,
    _handle_start,
    _handle_stop,
    _handle_toggle_cell,
    websocket_endpoint,
)

EMPTY_DIFF = {"birth": [], "death": []}


def _app():
    return SimpleNamespace(
        state=SimpleNamespace(runner=SimpleNamespace(schedule=AsyncMock()))
    )


@pytest.mark.asyncio
async def test_handle_start_returns_empty_diff():
    controller = Controller()

    result = await _handle_start(controller, {}, _app(), "client-1")

    assert result == EMPTY_DIFF


@pytest.mark.asyncio
async def test_handle_stop_returns_empty_diff():
    controller = Controller()

    result = await _handle_stop(controller, {}, _app(), "client-1")

    assert result == EMPTY_DIFF


@pytest.mark.asyncio
async def test_handle_set_speed_returns_empty_diff():
    controller = Controller()

    result = await _handle_set_speed(controller, {"speed": 2}, _app(), "client-1")

    assert result == EMPTY_DIFF


@pytest.mark.asyncio
async def test_handle_set_rules_returns_empty_diff():
    controller = Controller()

    result = await _handle_set_rules(
        controller, {"birth": [3], "survive": [2, 3]}, _app(), "client-1"
    )

    assert result == EMPTY_DIFF


@pytest.mark.asyncio
async def test_handle_start_does_not_leak_stale_next_step_diff():
    """Non-régression : un next_step précédent ne doit pas polluer le diff
    retourné par start/stop (bug historique du push en dur)."""
    controller = Controller()
    controller.game.toggle_cell(5, 5)
    controller.game.toggle_cell(6, 5)
    controller.game.toggle_cell(7, 5)
    controller.game.next_step()
    assert controller.game.birth or controller.game.death

    result = await _handle_start(controller, {}, _app(), "client-1")

    assert result == EMPTY_DIFF


@pytest.mark.asyncio
async def test_handle_stop_does_not_leak_stale_next_step_diff():
    controller = Controller()
    controller.game.toggle_cell(5, 5)
    controller.game.toggle_cell(6, 5)
    controller.game.toggle_cell(7, 5)
    controller.game.next_step()
    assert controller.game.birth or controller.game.death

    result = await _handle_stop(controller, {}, _app(), "client-1")

    assert result == EMPTY_DIFF


@pytest.mark.asyncio
async def test_handle_toggle_cell_birth_diff():
    controller = Controller()

    result = await _handle_toggle_cell(controller, {"x": 3, "y": 4}, _app(), "client-1")

    assert result == {"birth": [[3, 4]], "death": []}
    assert controller.game.is_alive(3, 4)


@pytest.mark.asyncio
async def test_handle_toggle_cell_death_diff():
    controller = Controller()
    controller.game.toggle_cell(3, 4)

    result = await _handle_toggle_cell(controller, {"x": 3, "y": 4}, _app(), "client-1")

    assert result == {"birth": [], "death": [[3, 4]]}
    assert not controller.game.is_alive(3, 4)


@pytest.mark.asyncio
async def test_handle_next_step_returns_matching_diff():
    controller = Controller()
    controller.game.toggle_cell(5, 5)
    controller.game.toggle_cell(6, 5)
    controller.game.toggle_cell(7, 5)

    result = await _handle_next_step(controller, {}, _app(), "client-1")

    assert result != EMPTY_DIFF
    for x, y in result["birth"]:
        assert controller.game.is_alive(x, y)
    for x, y in result["death"]:
        assert not controller.game.is_alive(x, y)


@pytest.mark.asyncio
async def test_handle_reset_returns_full_state():
    controller = Controller()
    controller.game.toggle_cell(1, 1)

    result = await _handle_reset(controller, {}, _app(), "client-1")

    assert set(result.keys()) == {"width", "height", "grid"}
    assert result["grid"] == []


@pytest.mark.asyncio
async def test_handle_grid_size_returns_full_state():
    controller = Controller()

    result = await _handle_grid_size(
        controller, {"width": 42, "height": 24}, _app(), "client-1"
    )

    assert set(result.keys()) == {"width", "height", "grid"}
    assert result == controller.game.get_grid_full_state()


class _FakeWebSocket:  # pylint: disable=too-few-public-methods
    def __init__(self, messages):
        self._messages = list(messages)
        self.app = None

    async def receive_json(self):
        if not self._messages:
            raise WebSocketDisconnect()
        return self._messages.pop(0)


def _endpoint_app(controller, persist_side_effect=None):
    session_manager = SimpleNamespace(
        get_or_create=AsyncMock(return_value=controller),
        persist=AsyncMock(side_effect=persist_side_effect),
        remove=lambda _client_id: None,
    )
    ws_manager = SimpleNamespace(
        connect=AsyncMock(), send=AsyncMock(), disconnect=lambda _client_id: None
    )
    runner = SimpleNamespace(schedule=AsyncMock())
    return SimpleNamespace(
        state=SimpleNamespace(
            session_manager=session_manager, ws_manager=ws_manager, runner=runner
        )
    )


@pytest.mark.asyncio
async def test_websocket_endpoint_processes_message_then_disconnects():
    controller = Controller()
    app = _endpoint_app(controller)
    ws = _FakeWebSocket([{"type": "set_speed", "speed": 2}])
    ws.app = app

    await websocket_endpoint(ws, client_id="client-1")

    app.state.session_manager.get_or_create.assert_awaited_once_with("client-1")
    app.state.ws_manager.connect.assert_awaited_once_with(ws, "client-1")
    assert app.state.ws_manager.send.await_count == 2
    assert controller.get_speed() == 2
    app.state.session_manager.persist.assert_awaited()


@pytest.mark.asyncio
async def test_websocket_endpoint_sends_full_state_for_unknown_message_type():
    controller = Controller()
    app = _endpoint_app(controller)
    ws = _FakeWebSocket([{"type": "unknown"}])
    ws.app = app

    await websocket_endpoint(ws, client_id="client-2")

    last_payload = app.state.ws_manager.send.await_args_list[-1].args[1]
    assert last_payload["grid"] == controller.game.get_grid_full_state()


@pytest.mark.asyncio
async def test_websocket_endpoint_generates_client_id_when_absent():
    controller = Controller()
    app = _endpoint_app(controller)
    ws = _FakeWebSocket([])
    ws.app = app

    await websocket_endpoint(ws, client_id=None)

    generated_id = app.state.session_manager.get_or_create.await_args.args[0]
    assert generated_id


@pytest.mark.asyncio
async def test_websocket_endpoint_swallows_persist_error_on_disconnect():
    controller = Controller()
    app = _endpoint_app(controller, persist_side_effect=RuntimeError("db down"))
    ws = _FakeWebSocket([])
    ws.app = app

    await websocket_endpoint(ws, client_id="client-3")
