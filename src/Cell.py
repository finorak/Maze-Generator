"""
Module containing the cell class
"""

NORTH = 0b1000


class Cell:
    """
    The cell class
    """
    def __init__(self, row: int, col: int, defaul_wall: int = 0b0000) -> None:
        """
        :param row: the row of the cell
        :type row: int
        :param col: the column of the cell
        :param row: int
        :rtype None
        """
        self.wall = defaul_wall
        self.row = row
        self.col = col
        self.visited = False
        self.is_42_cell = False

    def remove_wall(self, wall: str):
        if wall.lower() == "north" or self.wall.lower == "n":
            if self.wall & NORTH:
                self.wall = self.wall - NORTH

    def add_wall(self, wall):
        if wall.lower() == "north" or self.wall.lower == "n":
            self.wall = self.wall | NORTH

