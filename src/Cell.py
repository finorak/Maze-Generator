"""
Module containing the cell class
"""
from typing import Any

from .Image import Image
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
        self.image: Any = None
        self.color = 0xFFFFFF00
        self.initiated = False

    def _init(self, mlx: Any, mlx_ptr: Any) -> None:
        if self.initiated:
            return
        self.initiated = True
        self.image = Image()
        self.image.width = self.width
        self.image.height = self.height
        self.image.img = mlx.mlx_new_image(mlx_ptr,
                                           self.image.width,
                                           self.image.height)
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

    def add_wall(self, wall: str) -> None:
        wall = wall.lower()
        if wall == "north" or wall == "n":
            self.wall |= NORTH

    def draw_cell(self, mlx: Any, mlx_ptr: Any, mlx_win: Any) -> None:
        self._init(mlx, mlx_ptr)
        addr = mlx.mlx_get_data_addr(self.image.img)
        self.image.data, self.image.bpp, self.sl, _ = addr
        byte_per_pixel = self.image.bpp // 8
        for j in range(self.height):
            for i in range(self.width):
                offset = j * self.image.sl + i * byte_per_pixel
                self.image.data[offset:offset + 4] = self.color.to_bytes(4, 'little')
        mlx.mlx_put_image_to_window(mlx_ptr, mlx_win, self.image.img,
                                    self.row * self.width, self.col * self.height)
