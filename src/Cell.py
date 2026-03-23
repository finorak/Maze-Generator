"""
Module containing the cell class
"""
from typing import Any
from . import NORTH, SOUTH, WEST, EAST


class Cell:
    """
    The cell class
    """
    def __init__(self, row: int, col: int,
                 width: int, height: int,
                 win_width: int, win_height: int,
                 defaul_wall: int = 0b0000) -> None:
        """
        :param row: the row of the cell
        :type row: int
        :param col: the column of the cell
        :param row: int
        :rtype None
        """
        self.wall = defaul_wall
        # where to put the cell
        self.row = row
        self.col = col
        # the width of the cell
        self.width = width
        self.height = height
        # we use these two attribute to determine where
        # to draw the cell
        self.win_width = win_width
        self.win_height = win_height
        self.visited = False
        self.is_42_cell = False

    def remove_wall(self, wall: str) -> None:
        if wall.lower() == "north" or wall.lower() == "n":
            if self.wall & NORTH:
                self.wall -= NORTH
        if wall.lower() == "west" or wall.lower() == "w":
            if self.wall & WEST:
                self.wall -= WEST
        if wall.lower() == "south" or wall.lower() == "s":
            if self.wall & SOUTH:
                self.wall -= SOUTH
        if wall.lower() == "east" or wall.lower() == "e":
            if self.wall & EAST:
                self.wall -= EAST

    def add_wall(self, wall: str) -> None:
        if wall.lower() == "north" or wall.lower() == "n":
            self.wall |= NORTH

    def draw_cell(self, win: Any) -> None:
        print(self.row, self.col)
