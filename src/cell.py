"""
Module containing the cell class
"""


class Cell:
    """
    The cell class
    """
    def __init__(self, row: int, col: int) -> None:
        """
        :param row: the row of the cell
        :type row: int
        :param col: the column of the cell
        :param row: int
        :rtype None
        """
        self.row = row
        self.col = col
        self.visited = False
