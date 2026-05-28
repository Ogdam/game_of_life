from fastapi import WebSocket

class WSManager:
    def __init__(self):
        self.clients: dict = {}

    async def connect(self, ws: WebSocket, client_id: str):
        await ws.accept()
        self.clients[client_id] = ws

    def disconnect(self, client_id: str):
        self.clients.pop(client_id, None)
           
    async def send(self, client_id: str, data: dict):
        try:
            ws = self.clients.get(client_id)
            if ws:
                await ws.send_json(data)
        except Exception:
            self.disconnect(client_id)