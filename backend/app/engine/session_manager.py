from app.db.repository import load_session, upsert_session
from app.engine.controller import Controller


class SessionManager:
    def __init__(self, db_sessionmaker):
        self.controllers = {}
        self._db_sessionmaker = db_sessionmaker

    async def get_or_create(self, client_id):
        if client_id in self.controllers:
            return self.controllers[client_id]

        async with self._db_sessionmaker() as db:
            controller = await load_session(db, client_id) or Controller()

        self.controllers[client_id] = controller
        return controller

    async def persist(self, client_id):
        controller = self.controllers.get(client_id)
        if controller is None:
            return

        async with self._db_sessionmaker() as db:
            await upsert_session(client_id, controller, db)
            await db.commit()

    def remove(self, client_id):
        self.controllers.pop(client_id, None)
