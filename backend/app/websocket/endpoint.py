import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    app = websocket.app
    
    client_id = str(uuid.uuid4())
    controller = app.state.session_manager.get_or_create(client_id)
    await app.state.ws_manager.connect(websocket, client_id)

    try:
        while True:
            
            message = await websocket.receive_json()

            msg_type = message.get("type")

            # ---- RECEPTION CLIENT → SERVEUR ----
            if msg_type == "start":
                if not controller.get_scheduled():
                    controller.run()
                    print(controller.get_scheduled())
                    await app.state.runner.schedule(client_id, controller)

            elif msg_type == "stop":
               controller.pause()

            elif msg_type == "reset":
                controller.reset()
                
            elif msg_type == "set_speed":
                speed = message["speed"]
                controller.set_speed(speed)

            elif msg_type == "toggle_cell":
                x = message["x"]
                y = message["y"]
                controller.game.toggle_cell(x, y)
                
            elif msg_type == "next_step":
                controller.game.next_step()

            # ---- PUSH SERVEUR → CLIENT ----
            await app.state.ws_manager.send(client_id, {
                "status": controller.get_status(),
                "grid": controller.game.get_grid_full_state(),
            })

    except WebSocketDisconnect:
        app.state.ws_manager.disconnect(client_id)
        app.state.session_manager.remove(client_id)