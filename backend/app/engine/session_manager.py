from app.engine.controller import Controller


class SessionManager:
    def __init__(self):
        self.controllers = {}
        
    def get_or_create(self, client_id):
        if client_id not in self.controllers:
            self.controllers[client_id] = Controller()
        return self.controllers[client_id]
    
    def remove(self, client_id):
        self.controllers.pop(client_id, None)