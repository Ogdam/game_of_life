from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import SessionModel
from app.engine.controller import Controller, State


async def load_session(db: AsyncSession, client_id: str) -> Controller | None:
    row = await db.get(SessionModel, client_id)
    if row is None:
        return None

    controller = Controller(height=row.height, width=row.width)
    controller.state = State(row.state)
    controller.speed = row.speed
    controller.tick = row.tick
    controller.game.grid = {tuple(point) for point in row.grid}
    controller.set_rules({"birth": row.rules["birth"], "survive": row.rules["survive"]})
    return controller


async def upsert_session(client_id: str, controller: Controller, db: AsyncSession):
    values = {
        "client_id": client_id,
        "width": controller.game.width,
        "height": controller.game.height,
        "state": controller.get_status(),
        "speed": controller.get_speed(),
        "tick": controller.get_tick(),
        "grid": list(controller.game.grid),
        "rules": {
            "birth": list(controller.get_rules()["birth"]),
            "survive": list(controller.get_rules()["survive"]),
        },
    }
    stmt = insert(SessionModel).values(**values)
    stmt = stmt.on_conflict_do_update(
        index_elements=[SessionModel.client_id],
        set_={key: value for key, value in values.items() if key != "client_id"},
    )
    await db.execute(stmt)
