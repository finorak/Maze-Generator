from typing import Any
from src.setting import BLOCK_42_COLOR, CELL_COLOR, VISITED_COLOR
from src.utils.color_genertor import rgb
from .Cell import Cell
from . import DIRECTIONS
from random import choice, shuffle

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
                Cell(i, j, self.cols, self.rows) for j in range(self.rows)
            ] for i in range(self.cols)
        ]
        self.make_42_block()

    def make_42_block(self):
        def set_four(x: int, y: int) -> None:
            for i in range(3):
                self.data[x][y + i].is_42_cell = True
                self.data[x][y + i].color = BLOCK_42_COLOR
                self.data[x + 2][y + 2 + i].is_42_cell = True
                self.data[x + 2][y + 2 + i].color = BLOCK_42_COLOR
            self.data[x + 1][y + 2].is_42_cell = True
            self.data[x + 1][y + 2].color = BLOCK_42_COLOR

        def set_two(x: int, y: int) -> None:
            for i in range(3):
                self.data[x + i][y].is_42_cell = True
                self.data[x + i][y].color = BLOCK_42_COLOR
                self.data[x + i][y + 2].is_42_cell = True
                self.data[x + i][y + 2].color = BLOCK_42_COLOR
                self.data[x + i][y + 4].is_42_cell = True
                self.data[x + i][y + 4].color = BLOCK_42_COLOR
            self.data[x + 2][y + 1].is_42_cell = True
            self.data[x + 2][y + 1].color = BLOCK_42_COLOR
            self.data[x][y + 3].is_42_cell = True
            self.data[x][y + 3].color = BLOCK_42_COLOR

        set_four(self.cols//2 - 3, self.rows//2 - 2)
        set_two(self.cols//2 + 1, self.rows//2 - 2)

    def find_neighbor_closed(self,
                             cell_coord: tuple[int, int]
                             ) -> list[tuple[str, str, int, int]]:
        neighbors: list[tuple[str, str, int, int]] = []
        x, y = cell_coord
        if (x + 1 < self.cols and (self.data[x + 1][y].wall_closed \
                and not self.data[x + 1][y].is_42_cell)):
            neighbors.append(("e", "w", x + 1, y))
        if (x - 1 >= 0 and (self.data[x - 1][y].wall_closed and not \
                self.data[x - 1][y].is_42_cell)):
            neighbors.append(("w", "e", x - 1, y))
        if (y + 1 < self.rows and (self.data[x][y + 1].wall_closed \
                and not self.data[x][y + 1].is_42_cell)):
            neighbors.append(("n", "s", x, y + 1))
        if (y - 1 >= 0 and (self.data[x][y - 1].wall_closed and not \
                self.data[x][y - 1].is_42_cell)):
            neighbors.append(("s", "n", x, y - 1))
        return neighbors

    def generete(self):
        self.entry_pos = self.parent.config.get('entry')
        self.end_pos = self.parent.config.get('exit')
        if self.perfect:
            self.generate_perfect_mage()
        else:
            print("solve")
            self.generate_non_perfect_maze(self.entry_pos)

    def generate_perfect_mage(self, x = 0, y = 0):
        self.data[x][y].wall_closed = False
        neighbors = self.find_neighbor_closed((x, y))

        neighbor = random.choice(neighbors)
        wall1, wall2, new_x, new_y = neighbor
        self.data[x][y].remove_wall(wall1)
        self.parent.draw_cell(self.data[x][y])
        self.data[new_x][new_y].remove_wall(wall2)
        self.parent.draw_cell(self.data[new_x][new_y])
        self.generate_perfect_mage(new_x, new_y)

    def generate_non_perfect_maze(self,
                                  start_pos: tuple[int, int]
                                  ) -> None:
        self.data[0][0].color = VISITED_COLOR
        self.parent.draw_cell(self.data[0][0])
