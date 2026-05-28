import asyncio

from fastapi import FastAPI
from contextlib import asynccontextmanager

from websocket.dispatcher import ws_dispatcher
from engine.session_manager import SessionManager
from engine.runner import Runner

from api.rest import router as rest_router

from websocket.manager import WSManager
from websocket.endpoint import router as ws_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.event_queue = asyncio.Queue()
    app.state.ws_manager = WSManager()
    app.state.session_manager = SessionManager()
    app.state.runner = Runner(app.state.session_manager, app.state.event_queue)
    await app.state.runner.start()
    
    app.state.dispatcher_task = asyncio.create_task(
        ws_dispatcher(app)
    )
    
    yield
    app.state.runner.stop()
    app.state.dispatcher_task.cancel()
    try:
        await app.state.dispatcher_task
    except asyncio.CancelledError:
        pass
    
app = FastAPI(
    title="GAME_OF_LIFE_BK",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(ws_router)
app.include_router(rest_router)
