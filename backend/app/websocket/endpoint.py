import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


async def _handle_start(controller, _message, app, client_id):
    if not controller.get_scheduled():
        controller.run()
        await app.state.runner.schedule(client_id, controller)


async def _handle_stop(controller, _message, _app, _client_id):
    controller.pause()


async def _handle_reset(controller, _message, _app, _client_id):
    controller.reset()


async def _handle_set_speed(controller, message, _app, _client_id):
    controller.set_speed(message["speed"])


async def _handle_toggle_cell(controller, message, _app, _client_id):
    controller.game.toggle_cell(message["x"], message["y"])


async def _handle_grid_size(controller, message, _app, _client_id):
    controller.game.set_size(message["width"], message["height"])


async def _handle_next_step(controller, _message, _app, _client_id):
    controller.game.next_step()


MESSAGE_HANDLERS = {
    "start": _handle_start,
    "stop": _handle_stop,
    "reset": _handle_reset,
    "set_speed": _handle_set_speed,
    "toggle_cell": _handle_toggle_cell,
    "grid_size": _handle_grid_size,
    "next_step": _handle_next_step,
}


async def _process_message(msg_type, controller, message, app, client_id):
    handler = MESSAGE_HANDLERS.get(msg_type)
    if handler:
        await handler(controller, message, app, client_id)


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
            print(msg_type)

            # ---- RECEPTION CLIENT → SERVEUR ----
            await _process_message(msg_type, controller, message, app, client_id)

            # ---- PUSH SERVEUR → CLIENT ----
            await app.state.ws_manager.send(
                client_id,
                {
                    "status": controller.get_status(),
                    "tick": controller.get_tick(),
                    "grid": controller.game.get_grid_full_state(),
                },
            )

    except WebSocketDisconnect:
        app.state.ws_manager.disconnect(client_id)
        app.state.session_manager.remove(client_id)
