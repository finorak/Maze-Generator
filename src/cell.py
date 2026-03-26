"""
Module containing the cell class
"""
from random import seed
from typing import Any, Self
from src.setting import CELL_COLOR
from .image import Image
from . import NORTH, SOUTH, WEST, EAST

class Cell:
    def __init__(self, row: int, col: int,
                 rows: int, cols: int, size: int = 40,
                 color: int = CELL_COLOR) -> None:
        self.row = row
        self.col = col
        self.rows = row
        self.cols = cols
        self.color = color
        self.wall = 0b1111
        self.is_42_cell = False
        self.is_visited = False
        self.wall_closed = True
        self.size = size
        self.image: Any = Image()

    def remove_wall(self, wall: str) -> None:
        wall = wall.lower()
        if (wall == "north" or wall == "n"):
            if self.wall & NORTH:
                self.wall -= NORTH
        if (wall == "west" or wall == "w"):
            if self.wall & WEST:
                self.wall -= WEST
        if (wall == "south" or wall == "s"):
            if self.wall & SOUTH:
                self.wall -= SOUTH
        if wall == "east" or wall == "e":
            if self.wall & EAST:
                self.wall -= EAST

    def get_neightboors(self, cells: list[list[Self]]) -> list[Self]:
        neighbors: list[Self] = []
        x, y = self.row, self.col
        if (x + 1 < self.cols and not cells[x + 1][y].is_visited \
                and not cells[x + 1][y].is_42_cell):
            neighbors.append(cells[x + 1][y])
        if (x - 1 >= 0 and not cells[x - 1][y].is_visited \
                and not cells[x - 1][y].is_42_cell):
            neighbors.append(cells[x - 1][y])
        if (y <= self.rows - 1 and not cells[x][y + 1].is_visited \
                                    and not cells[x][y + 1].is_42_cell):
            neighbors.append(cells[x][y + 1])
        if (y - 1 >= 0 and not cells[x][y - 1].is_visited \
            and not cells[x][y - 1].is_42_cell):
            neighbors.append(cells[x][y - 1])
        return neighbors
