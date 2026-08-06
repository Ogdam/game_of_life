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
