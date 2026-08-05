from app.engine.rules import next_generation


class GameState:

    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.grid = set()
        self.birth = set()
        self.death = set()

    def reset_grid(self):
        self.grid = set()

    def set_size(self, height: int, width: int):
        self.height = height
        self.width = width

    def toggle_cell(self, x: int, y: int):
        if (x, y) in self.grid:
            self.grid.discard((x, y))
        else:
            self.grid.add((x, y))

    def is_alive(self, x: int, y: int):
        return (x, y) in self.grid

    def get_grid_state(self):
        return {"birth": list(self.birth), "death": list(self.death)}

    def get_grid_full_state(self):
        return {
            "width": self.width,
            "height": self.height,
            "grid": list(self.grid),
        }

    def next_step(self):
        self.grid, self.birth, self.death = next_generation(self.grid)
