import uuid
from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect

router = APIRouter()

MAX_NEIGHBORS = 8
VALID_NEIGHBOR_COUNTS = range(0, MAX_NEIGHBORS + 1)


def _sanitize_rule_values(values) -> set[int]:
    return {v for v in values if isinstance(v, int) and v in VALID_NEIGHBOR_COUNTS}


def _serialize_rules(controller) -> dict:
    rules = controller.get_rules()
    return {"birth": list(rules["birth"]), "survive": list(rules["survive"])}


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


async def _handle_set_rules(controller, message, _app, _client_id):
    birth = _sanitize_rule_values(message["birth"])
    survive = _sanitize_rule_values(message["survive"])
    controller.set_rules({"birth": birth, "survive": survive})


MESSAGE_HANDLERS = {
    "start": _handle_start,
    "stop": _handle_stop,
    "reset": _handle_reset,
    "set_speed": _handle_set_speed,
    "toggle_cell": _handle_toggle_cell,
    "grid_size": _handle_grid_size,
    "next_step": _handle_next_step,
    "set_rules": _handle_set_rules,
}


async def _process_message(msg_type, controller, message, app, client_id):
    handler = MESSAGE_HANDLERS.get(msg_type)
    if handler:
        await handler(controller, message, app, client_id)


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, client_id: str | None = Query(default=None)
):
    app = websocket.app

    client_id = client_id or str(uuid.uuid4())
    controller = await app.state.session_manager.get_or_create(client_id)
    await app.state.ws_manager.connect(websocket, client_id)

    await app.state.ws_manager.send(
        client_id,
        {
            "type": "client_id",
            "client_id": client_id,
            "status": controller.get_status(),
            "tick": controller.get_tick(),
            "grid": controller.game.get_grid_full_state(),
            "rules": _serialize_rules(controller),
        },
    )

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
                    "rules": _serialize_rules(controller),
                },
            )

            await app.state.session_manager.persist(client_id)

    except WebSocketDisconnect:
        try:
            await app.state.session_manager.persist(client_id)
        except Exception:  # pylint: disable=broad-exception-caught
            # Best-effort persistence on disconnect: ne doit jamais empêcher
            # le nettoyage de la session (cf. dispatcher.py/manager.py).
            pass
        app.state.ws_manager.disconnect(client_id)
        app.state.session_manager.remove(client_id)
