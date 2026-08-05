from types import SimpleNamespace

from api.rest import get_status
from engine.controller import Controller, State


def _request(clients=None, controllers=None):
    state = SimpleNamespace(
        ws_manager=SimpleNamespace(clients=clients or {}),
        session_manager=SimpleNamespace(controllers=controllers or {}),
    )
    return SimpleNamespace(app=SimpleNamespace(state=state))


def test_get_status_counts_connections_and_sessions():
    running = Controller()
    running.state = State.RUNNING
    paused = Controller()

    request = _request(
        clients={"a": object(), "b": object()},
        controllers={"a": running, "b": paused},
    )

    result = get_status(request)

    assert result.active_connections == 2
    assert result.active_sessions == 2
    assert result.running_sessions == 1
    assert result.paused_sessions == 1


def test_get_status_empty_server():
    result = get_status(_request())

    assert result.active_connections == 0
    assert result.active_sessions == 0
    assert result.running_sessions == 0
    assert result.paused_sessions == 0
