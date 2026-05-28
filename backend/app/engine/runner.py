import asyncio
import heapq
import time

from engine.session_manager import SessionManager
from engine.controller import State


class Runner():

    def __init__(self, session_manager: SessionManager, event_queue: asyncio.Queue):
        self.session_manager = session_manager
        self.event_queue = event_queue
        self.running = True
        self._task = None
        self._heap = []
                
    async def start(self):
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self.loop())
                        
    async def schedule(self, client_id, controller):
        if controller.get_status() == State.RUNNING.value and controller.get_scheduled():
            now = time.perf_counter()

            controller.next_tick = now + controller.speed
            controller.scheduled = True

            heapq.heappush(
                self._heap,
                (controller.next_tick, client_id)
            )

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
                    await self.event_queue.put({
                        "client_id": client_id,
                        "data": {
                            "tick": controller.get_tick(),
                            "status": controller.get_status(),
                            "grid": controller.game.get_grid_state(),
                        }
                    })

                    next_tick = controller.next_tick + controller.speed
                    controller.next_tick = next_tick

                    heapq.heappush(self._heap, (next_tick, client_id))

        except asyncio.CancelledError:
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