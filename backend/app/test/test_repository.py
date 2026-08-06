# pylint: disable=redefined-outer-name
# Les paramètres de test nommés comme la fixture `db_sessionmaker` sont le
# mécanisme d'injection standard de pytest, pas une variable masquée par erreur.
import os

import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from db.base import Base
from db.engine import create_session_factory
from db.repository import load_session, upsert_session
from engine.controller import Controller

DATABASE_URL = os.getenv("DATABASE_URL")


async def _is_reachable(database_url: str) -> bool:
    engine = create_async_engine(database_url)
    try:
        async with engine.connect():
            return True
    except Exception:  # pylint: disable=broad-exception-caught
        return False
    finally:
        await engine.dispose()


requires_postgres = pytest.mark.skipif(
    not DATABASE_URL, reason="DATABASE_URL n'est pas défini : DB non disponible"
)


@pytest.fixture
async def db_sessionmaker():
    if not DATABASE_URL or not await _is_reachable(DATABASE_URL):
        pytest.skip("Postgres non joignable via DATABASE_URL")

    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    sessionmaker = create_session_factory(engine)
    yield sessionmaker

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@requires_postgres
@pytest.mark.asyncio
async def test_upsert_then_load_round_trip(db_sessionmaker):
    controller = Controller(height=10, width=10)
    controller.run()
    controller.set_speed(2)
    controller.tick = 5
    controller.game.toggle_cell(1, 1)
    controller.game.toggle_cell(2, 2)

    async with db_sessionmaker() as db:
        await upsert_session("client-round-trip", controller, db)
        await db.commit()

    async with db_sessionmaker() as db:
        loaded = await load_session(db, "client-round-trip")

    assert loaded is not None
    assert loaded.get_status() == "running"
    assert loaded.get_speed() == 2
    assert loaded.get_tick() == 5
    assert loaded.game.grid == {(1, 1), (2, 2)}
    assert loaded.game.width == 10
    assert loaded.game.height == 10


@requires_postgres
@pytest.mark.asyncio
async def test_load_session_returns_none_when_absent(db_sessionmaker):
    async with db_sessionmaker() as db:
        loaded = await load_session(db, "unknown-client")

    assert loaded is None
