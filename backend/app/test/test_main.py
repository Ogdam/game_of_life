from unittest.mock import AsyncMock

import pytest

import main


class _FakeEngine:  # pylint: disable=too-few-public-methods
    def __init__(self):
        self.dispose = AsyncMock()


@pytest.mark.asyncio
async def test_lifespan_starts_and_stops_runner(monkeypatch):
    fake_engine = _FakeEngine()
    monkeypatch.setattr(main, "create_db_engine", lambda: fake_engine)
    monkeypatch.setattr(main, "create_session_factory", lambda engine: lambda: None)

    async with main.lifespan(main.app):
        assert main.app.state.runner.is_running()
        assert main.app.state.db_engine is fake_engine

    assert not main.app.state.runner.is_running()
    fake_engine.dispose.assert_awaited_once()
