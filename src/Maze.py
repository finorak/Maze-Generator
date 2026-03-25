from typing import Any

from src.setting import BLOCK_42_COLOR, CELL_COLOR, VISITED_COLOR
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
        # self.perfect = parent.config.get("perferct")
        self.perfect = False

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

    def find_neighbor_closed(self, cell_coord: tuple[int, int]) -> list[tuple[int, int]]:
        neighbors: list[tuple[int, int]] = []
        x, y = cell_coord
        if (x + 1 < self.cols and self.data[x + 1][y].wall_closed):
            neighbors.append(("right", x + 1, y))
        if (x - 1 >= 0 and self.data[x - 1][y].wall_closed):
            neighbors.append(("left", x - 1, y))
        if (y + 1 < self.rows and self.data[x][y + 1].wall_closed):
            neighbors.append(("up", x, y + 1))
        if (y - 1 >= 0 and self.data[x][y - 1].wall_closed):
            neighbors.append(("down", x, y - 1))
        return neighbors

    def generete(self):
        self.entry_pos = self.parent.config.get('entry')
        self.end_pos = self.parent.config.get('exit')
        if self.perfect:
            self.generate_perfect_mage()
        else:
            self.generate_non_perfect_mage(self.entry_pos,
                                           self.entry_pos,
                                           self.end_pos)

    def generate_perfect_mage(self, x = 0, y = 0):
        self.data[x][y].wall_closed = False
        neighbors = self.find_neighbor_closed((x, y))

        while len(neighbors) != 0:
            direction, new_x, new_y = random.choice(neighbors)

    def generate_non_perfect_mage(self, curr_pos: tuple[int, int],
                                  start_pos: tuple[int, int],
                                  end_pos: tuple[int, int]) -> None:
        def generate_maze(curr_pos: tuple[int, int]) -> None:
            curr_cell = self.data[curr_pos[0]][curr_pos[1]]
            if curr_cell.is_42_cell:
                return None

        generate_maze(curr_pos)
