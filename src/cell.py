"""
Module containing the cell class
"""

from typing import Any
from .image import Image
from .setting import (
        NORTH, SOUTH, WEST,
        EAST, WALL_COLORS, CELL_SIZE,
        )


class Cell:
    def __init__(
        self,
        row: int,
        col: int,
        size: int = CELL_SIZE,
        color: int = WALL_COLORS[0],
    ) -> None:
        self.row = row
        self.col = col
        self._color = color
        self._wall = 0b1111
        self.is_42_cell = False
        self.is_visited = False
        self.wall_closed = True
        self.size = size
        self.image: Any = Image()
        self.parent: tuple[int, int] | Any = None
        self.updated: bool = False

    @property
    def color(self) -> int:
        return self._color

    @color.setter
    def color(self, color: int) -> None:
        self.updated = False
        self._color = color

    @property
    def wall(self) -> int:
        return self._wall

    @wall.setter
    def wall(self, wall: int) -> None:
        self.updated = False
        self._wall = wall

    def remove_wall(self, wall: str) -> None:
        wall = wall.lower()
        if self.is_42_cell:
            return None
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
        self.updated = False
