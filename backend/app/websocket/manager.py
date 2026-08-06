import logging

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class WSManager:
    def __init__(self):
        self.clients: dict = {}

    async def connect(self, ws: WebSocket, client_id: str):
        await ws.accept()
        self.clients[client_id] = ws
        logger.info("WS connected: client_id=%s", client_id)

    def disconnect(self, client_id: str):
        self.clients.pop(client_id, None)
        logger.info("WS disconnected: client_id=%s", client_id)

    async def send(self, client_id: str, data: dict):
        try:
            ws = self.clients.get(client_id)
            if ws:
                await ws.send_json(data)
        except Exception:  # pylint: disable=broad-exception-caught
            logger.error("WS send failed: client_id=%s", client_id, exc_info=True)
            self.disconnect(client_id)
