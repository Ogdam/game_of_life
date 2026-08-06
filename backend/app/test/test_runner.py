import asyncio

import pytest

from engine.controller import Controller
from engine.runner import Runner


class _FakeSessionManager:  # pylint: disable=too-few-public-methods
    def __init__(self, controllers):
        self.controllers = controllers

    async def persist(self, _client_id):
        pass


@pytest.mark.asyncio
async def test_loop_stays_reactive_when_speed_is_not_strictly_positive():
    """Non-régression #42 : même si un controller se retrouve avec un speed
    <= 0 (contournement direct de l'attribut, hors set_speed), la boucle
    interne de Runner.loop() ne doit jamais accaparer l'event loop."""
    controller = Controller()
    controller.run()
    controller.speed = 0

    session_manager = _FakeSessionManager({"client-1": controller})
    runner = Runner(session_manager, asyncio.Queue())
    await runner.schedule("client-1", controller)

    heartbeats = 0

    async def _heartbeat():
        nonlocal heartbeats
        for _ in range(20):
            await asyncio.sleep(0.005)
            heartbeats += 1

    await runner.start()
    await asyncio.wait_for(_heartbeat(), timeout=2)

    await runner.stop()

    assert heartbeats == 20
    assert controller.get_tick() > 0
    assert not runner.is_running()


@pytest.mark.asyncio
async def test_loop_idles_without_crashing_when_heap_is_empty():
    runner = Runner(_FakeSessionManager({}), asyncio.Queue())

    await runner.start()
    await asyncio.sleep(0.05)
    await runner.stop()

    assert not runner.is_running()


@pytest.mark.asyncio
async def test_loop_skips_tick_when_scheduled_controller_is_missing():
    controller = Controller()
    controller.run()
    controller.set_speed(0.01)

    session_manager = _FakeSessionManager({})  # "client-1" absent du cache
    runner = Runner(session_manager, asyncio.Queue())
    await runner.schedule("client-1", controller)

    await runner.start()
    await asyncio.sleep(0.05)
    await runner.stop()

    assert not runner._heap  # pylint: disable=protected-access


@pytest.mark.asyncio
async def test_loop_skips_tick_when_controller_is_no_longer_running():
    controller = Controller()
    controller.run()
    controller.set_speed(0.01)

    session_manager = _FakeSessionManager({"client-1": controller})
    runner = Runner(session_manager, asyncio.Queue())
    await runner.schedule("client-1", controller)
    controller.pause()

    await runner.start()
    await asyncio.sleep(0.05)
    await runner.stop()

    assert not runner._heap  # pylint: disable=protected-access


@pytest.mark.asyncio
async def test_loop_logs_and_reraises_on_unexpected_exception():
    controller = Controller()
    controller.run()
    controller.set_speed(0.01)
    controller.step = lambda: (_ for _ in ()).throw(RuntimeError("boom"))

    session_manager = _FakeSessionManager({"client-1": controller})
    runner = Runner(session_manager, asyncio.Queue())
    await runner.schedule("client-1", controller)

    await runner.start()
    await asyncio.sleep(0.1)

    assert runner._task.done()  # pylint: disable=protected-access
    with pytest.raises(RuntimeError, match="boom"):
        await runner._task  # pylint: disable=protected-access


@pytest.mark.asyncio
async def test_persist_safely_swallows_persist_errors():
    class _FailingSessionManager:  # pylint: disable=too-few-public-methods
        async def persist(self, _client_id):
            raise RuntimeError("db down")

    runner = Runner(_FailingSessionManager(), asyncio.Queue())

    await runner._persist_safely("client-1")  # pylint: disable=protected-access


@pytest.mark.asyncio
async def test_stop_swallows_cancelled_error_raised_by_task():
    """Filet de sécurité de Runner.stop() : même si la tâche interne ne
    catche pas elle-même CancelledError (contrairement à loop()), stop()
    ne doit jamais propager l'annulation à l'appelant."""

    async def _never_ending():
        await asyncio.sleep(10)

    runner = Runner(_FakeSessionManager({}), asyncio.Queue())
    # pylint: disable-next=protected-access
    runner._task = asyncio.create_task(_never_ending())

    await runner.stop()

    assert runner._task is None  # pylint: disable=protected-access
