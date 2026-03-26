"""
Module containing the cell class
"""
from typing import Any
from typing_extensions import Self
from .Image import Image
from . import NORTH, SOUTH, WEST, EAST

class Cell:
    def __init__(self, row: int, col: int, size: int = 40) -> None:
        self.row = row
        self.col = col
        self.wall = 0b1111
        self.is_42_cell = False
        self.is_visited = False
        self.wall_closed = True
        self.size = size
        self.neightboors = []
        self.image: Any = Image()

    def remove_wall(self, wall: str) -> None:
        wall = wall.lower()
        if wall == "north" or wall == "n":
            if self.wall & NORTH:
                self.wall -= NORTH
        if wall == "west" or wall == "w":
            if self.wall & WEST:
                self.wall -= WEST
        if wall == "south" or wall == "s":
            if self.wall & SOUTH:
                self.wall -= SOUTH
        if wall == "east" or wall == "e":
            if self.wall & EAST:
                self.wall -= EAST

    def get_neightboor(self, cells: list[list[Self]],
                       rows: int, cols: int) -> None:
        self.neightboors = []
        if self.row < rows - 1:
            self.neightboors.append(cells[self.row + 1][self.col])
        elif self.row > 0:
            self.neightboors.append(cells[self.row - 1][self.col])
        elif self.col < cols - 1:
            self.neightboors.append(cells[self.row][self.col + 1])
        elif self.col > 0:
            self.neightboors.append(cells[self.row][self.col - 1])
