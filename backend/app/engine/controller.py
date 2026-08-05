from enum import Enum

from app.engine.game_state import GameState


class State(Enum):
    PAUSE = "pause"
    RUNNING = "running"


class Controller:

    def __init__(self, height=90, width=90):
        self.state = State.PAUSE
        self.speed = 1
        self.game = GameState(height, width)
        self.tick = 0
        self.scheduled = False

    def run(self):
        self.state = State.RUNNING
        self.scheduled = True

    def pause(self):
        self.state = State.PAUSE
        self.scheduled = False

    def reset(self):
        self.game.reset_grid()
        self.state = State.PAUSE
        self.scheduled = False
        self.tick = 0

    def set_speed(self, speed: int):
        self.speed = speed

    def get_scheduled(self):
        return self.scheduled

    def set_size(self, height: int, width: int):
        self.game.set_size(height, width)

    def step(self):
        if self.state == State.RUNNING:
            self.game.next_step()
            self.tick += 1

    def get_status(self):
        return self.state.value

    def get_tick(self):
        return self.tick

    def get_speed(self):
        return self.speed

    def set_rules(self, rules: dict):
        self.game.set_rules(rules)

    def get_rules(self):
        return self.game.rules
