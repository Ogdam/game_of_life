from pydantic import BaseModel


class ServerStatusResponse(BaseModel):
    active_connections: int
    active_sessions: int
    running_sessions: int
    paused_sessions: int
