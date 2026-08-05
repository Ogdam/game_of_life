from fastapi import APIRouter, Request

from app.engine.controller import State
from app.schemas.status import ServerStatusResponse

router = APIRouter()


@router.get("/status", response_model=ServerStatusResponse)
def get_status(request: Request) -> ServerStatusResponse:
    ws_manager = request.app.state.ws_manager
    session_manager = request.app.state.session_manager

    active_sessions = len(session_manager.controllers)
    running_sessions = sum(
        1
        for controller in session_manager.controllers.values()
        if controller.get_status() == State.RUNNING.value
    )

    return ServerStatusResponse(
        active_connections=len(ws_manager.clients),
        active_sessions=active_sessions,
        running_sessions=running_sessions,
        paused_sessions=active_sessions - running_sessions,
    )
