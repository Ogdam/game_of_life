from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

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
