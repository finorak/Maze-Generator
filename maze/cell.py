"""Cell object used to represent a maze grid location.

This module provides the `Cell` class which tracks wall bits, flags
and a small image buffer used for drawing.
"""

from typing import Any

from .image import Image


class Cell:
    """Represents a single cell in the maze grid.

    Attributes:
        row, col: grid coordinates.
        wall: 4-bit mask of walls (N,S,W,E).
    """
    def __init__(
        self,
        row: int,
        col: int,
        settings: Any,
    ) -> None:
        """Initialize a cell with default maze and rendering attributes.

        Args:
            row: Row index in the maze grid.
            col: Column index in the maze grid.
            settings: Settings module/object exposing constants.
        """
        self.init_attribute(row, col,
                            settings.CELL_SIZE,
                            settings.WALL_COLORS[0],
                            settings)

    def init_attribute(self,
                       row: int,
                       col: int,
                       size: int,
                       color: int,
                       settings: Any) -> None:
        """Attribute initiatiolasation for 'Cell'

        Args:
            row: the row where to place the cell
            col: the column where to place the cell
            size:the dimention of the size
            color:the color of the cell
        """
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
        self.settings = settings

    @property
    def color(self) -> int:
        """Color property
        """
        return self._color

    @color.setter
    def color(self, color: int) -> None:
        """Color setter

        Args:
            color: int
        """
        self.updated = False
        self._color = color

    @property
    def wall(self) -> int:
        """Wall property
        """
        return self._wall

    @wall.setter
    def wall(self, wall: int) -> None:
        """Wall setter

        Args:
            wall: int a binary ranging from [0, 15]
        """
        self.updated = False
        self._wall = wall

    def remove_wall(self, wall: str) -> None:
        """Remove a named wall from this cell.

        Args:
            wall: One of 'north', 'south', 'east', 'west' (or 'n','s','e','w').
        """
        wall = wall.lower()
        if self.is_42_cell:
            return None
        if wall in ("north", "n"):
            if self.wall & self.settings.NORTH:
                self.wall -= self.settings.NORTH
        if wall in ("west", "w"):
            if self.wall & self.settings.WEST:
                self.wall -= self.settings.WEST
        if wall in ("south", "s"):
            if self.wall & self.settings.SOUTH:
                self.wall -= self.settings.SOUTH
        if wall in ("east", "e"):
            if self.wall & self.settings.EAST:
                self.wall -= self.settings.EAST
        self.updated = False
