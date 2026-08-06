import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.logging_config import configure_logging
from app.websocket.dispatcher import ws_dispatcher
from app.db.engine import create_db_engine, create_session_factory
from app.engine.session_manager import SessionManager
from app.engine.runner import Runner

from app.api.rest import router as rest_router

from app.websocket.manager import WSManager
from app.websocket.endpoint import router as ws_router

configure_logging()


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    fastapi_app.state.event_queue = asyncio.Queue()
    fastapi_app.state.ws_manager = WSManager()

    fastapi_app.state.db_engine = create_db_engine()
    db_sessionmaker = create_session_factory(fastapi_app.state.db_engine)

    fastapi_app.state.session_manager = SessionManager(db_sessionmaker)
    fastapi_app.state.runner = Runner(
        fastapi_app.state.session_manager, fastapi_app.state.event_queue
    )
    await fastapi_app.state.runner.start()

    fastapi_app.state.dispatcher_task = asyncio.create_task(ws_dispatcher(fastapi_app))

    yield
    fastapi_app.state.runner.stop()
    fastapi_app.state.dispatcher_task.cancel()
    try:
        await fastapi_app.state.dispatcher_task
    except asyncio.CancelledError:
        pass
    await fastapi_app.state.db_engine.dispose()


app = FastAPI(title="GAME_OF_LIFE_BK", version="1.0.0", lifespan=lifespan)

app.include_router(ws_router)
app.include_router(rest_router)
