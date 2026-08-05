import asyncio
import heapq
import time

from app.engine.session_manager import SessionManager
from app.engine.controller import State


class Runner:

    def __init__(self, session_manager: SessionManager, event_queue: asyncio.Queue):
        self.session_manager = session_manager
        self.event_queue = event_queue
        self.running = True
        self._task = None
        self._heap = []
        self._background_tasks: set = set()

    async def start(self):
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self.loop())

    async def schedule(self, client_id, controller):
        if (
            controller.get_status() == State.RUNNING.value
            and controller.get_scheduled()
        ):
            now = time.perf_counter()

            controller.next_tick = now + controller.speed
            controller.scheduled = True

            heapq.heappush(self._heap, (controller.next_tick, client_id))

    async def loop(self):
        try:
            while self.running:
                now = time.perf_counter()

                if not self._heap:
                    await asyncio.sleep(0.05)
                    continue

                next_tick, _ = self._heap[0]
                sleep_time = max(0, next_tick - now)
                await asyncio.sleep(sleep_time)

                now = time.perf_counter()

                while self._heap and self._heap[0][0] <= now:
                    _, client_id = heapq.heappop(self._heap)

                    controller = self.session_manager.controllers.get(client_id)
                    if not controller:
                        continue

                    if controller.get_status() != State.RUNNING.value:
                        continue

                    controller.step()
                    await self.event_queue.put(
                        {
                            "client_id": client_id,
                            "data": {
                                "tick": controller.get_tick(),
                                "status": controller.get_status(),
                                "grid": controller.game.get_grid_state(),
                            },
                        }
                    )
                    self._schedule_persist(client_id)

                    next_tick = controller.next_tick + controller.speed
                    controller.next_tick = next_tick

                    heapq.heappush(self._heap, (next_tick, client_id))

        except asyncio.CancelledError:
            pass

    def _schedule_persist(self, client_id):
        task = asyncio.create_task(self._persist_safely(client_id))
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)

    async def _persist_safely(self, client_id):
        try:
            await self.session_manager.persist(client_id)
        except Exception:  # pylint: disable=broad-exception-caught
            # La persistance ne doit jamais casser la boucle de tick (hot path).
            pass

    async def stop(self):
        self.running = False
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        self._task = None

    def is_running(self):
        return self._task is not None and not self._task.done()
