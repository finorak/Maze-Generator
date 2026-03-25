from typing import Any
from .Cell import Cell
from . import DIRECTIONS
from random import shuffle

import random

class Maze:
    def __init__(self, parent: Any):
        self.data: list[list[Cell]] | Any = None
        self.rows = 0
        self.cols = 0
        self.parent = parent
        self.perfect = parent.config.get("perferct")

    def init_data(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.data = [
            [
                Cell(i, j) for j in range(self.rows)
            ] for i in range(self.cols)
        ]
        self.make_42_block()

    def make_42_block(self):
        def set_four(x: int, y: int) -> None:
            for i in range(3):
                self.data[x][y + i].is_42_cell = True
                self.data[x + 2][y + 2 + i].is_42_cell = True
            self.data[x + 1][y + 2].is_42_cell = True

        def set_two(x: int, y: int) -> None:
            for i in range(3):
                self.data[x + i][y].is_42_cell = True
                self.data[x + i][y + 2].is_42_cell = True
                self.data[x + i][y + 4].is_42_cell = True
            self.data[x + 2][y + 1].is_42_cell = True
            self.data[x][y + 3].is_42_cell = True

        set_four(self.cols//2 - 3, self.rows//2 - 2)
        set_two(self.cols//2 + 1, self.rows//2 - 2)

    def find_neighbor_closed(self, cell_coord: tuple[int, int]) -> list[tuple[str, str, int, int]]:
        neighbors: list[tuple[str, str, int, int]] = []
        x, y = cell_coord
        if (x + 1 < self.cols and self.data[x + 1][y].wall_closed):
            neighbors.append(("east", "west", x + 1, y))
        if (x - 1 >= 0 and self.data[x - 1][y].wall_closed):
            neighbors.append(("west", "east", x - 1, y))
        if (y + 1 < self.rows and self.data[x][y + 1].wall_closed):
            neighbors.append(("north", "south", x, y + 1))
        if (y - 1 >= 0 and self.data[x][y - 1].wall_closed):
            neighbors.append(("south", "north", x, y - 1))
        return neighbors

    def generete(self):
        entry_pos = self.parent.config.get('entry')
        end_pos = self.parent.config.get('exit')
        if self.perfect:
            self.generate_perfect_mage()
        else:
            self.generate_non_perfect_mage()

    def generate_perfect_mage(self, x = 0, y = 0):
        self.data[x][y].wall_closed = False
        neighbors = self.find_neighbor_closed((x, y))

        # while len(neighbors) != 0:
        neighbor = random.choice(neighbors)
        wall1, wall2, new_x, new_y = neighbor
        self.data[x][y].remove_wall(wall1)
        self.data[new_x][new_y].remove_wall(wall2)
        self.generate_perfect_mage(new_x, new_y)

    def generate_non_perfect_mage(self):
        pass
