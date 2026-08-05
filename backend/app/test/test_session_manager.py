from contextlib import asynccontextmanager
from unittest.mock import AsyncMock

import pytest

from engine.session_manager import SessionManager


class _FakeDbSession:  # pylint: disable=too-few-public-methods
    def __init__(self, get_result=None):
        self.get = AsyncMock(return_value=get_result)
        self.execute = AsyncMock()
        self.commit = AsyncMock()


def _sessionmaker(get_result=None):
    db_session = _FakeDbSession(get_result)

    @asynccontextmanager
    async def factory():
        yield db_session

    factory.db_session = db_session
    return factory


@pytest.mark.asyncio
async def test_get_or_create_cache_hit_returns_same_instance():
    manager = SessionManager(_sessionmaker())
    first = await manager.get_or_create("client-1")
    second = await manager.get_or_create("client-1")

    assert first is second


@pytest.mark.asyncio
async def test_get_or_create_cache_miss_creates_new_controller_when_db_empty():
    manager = SessionManager(_sessionmaker(get_result=None))

    controller = await manager.get_or_create("client-2")

    assert controller.get_tick() == 0
    assert manager.controllers["client-2"] is controller


@pytest.mark.asyncio
async def test_remove_pops_controller_from_cache():
    manager = SessionManager(_sessionmaker())
    await manager.get_or_create("client-3")

    manager.remove("client-3")

    assert "client-3" not in manager.controllers
