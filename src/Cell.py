"""
Module containing the cell class
"""
from typing import Any
from .Image import Image
from . import NORTH, SOUTH, WEST, EAST, WALL_THICK, CELL_COLOR, WALL_COLOR

class Cell:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.wall = 0b1111
        self.is_42_cell = False
        self.is_visited = False

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

# class Cell:
#     """
#     The cell class
#     """
#     def __init__(self, row: int, col: int,
#                  width: int, height: int,
#                  win_width: int, win_height: int,
#                  defaul_wall: int = 0b1111) -> None:
#         """
#         :param row: the row of the cell
#         :type row: int
#         :param col: the column of the cell
#         :param row: int
#         :rtype None
#         """
#         self.wall = defaul_wall
#         # where to put the cell
#         self.row = row
#         self.col = col
#         # the width of the cell
#         self.width = width
#         self.height = height
#         # we use these two attribute to determine where
#         # to draw the cell
#         self.win_width = win_width
#         self.win_height = win_height
#         self.visited = False
#         self.is_42_cell = False
#         self.image: Any = None
#         self.initiated = False

#     def _init(self, mlx: Any, mlx_ptr: Any, event_handler: Any) -> None:
#         if self.initiated:
#             return None
#         self.wall_initiated = False
#         self.event_handler = event_handler
#         self.initiated = True
#         self.image = Image()
#         self.image.width = self.width
#         self.image.height = self.height
#         self.image.img = mlx.mlx_new_image(mlx_ptr,
#                                            self.image.width,
#                                            self.image.height)

#     def remove_wall(self, wall: str) -> None:
#         wall = wall.lower()
#         if wall == "north" or wall == "n":
#             if self.wall & NORTH:
#                 self.wall -= NORTH
#         if wall == "west" or wall == "w":
#             if self.wall & WEST:
#                 self.wall -= WEST
#         if wall == "south" or wall == "s":
#             if self.wall & SOUTH:
#                 self.wall -= SOUTH
#         if wall == "east" or wall == "e":
#             if self.wall & EAST:
#                 self.wall -= EAST

#     def add_wall(self, wall: str) -> None:
#         wall = wall.lower()
#         if wall == "north" or wall == "n":
#             self.wall |= NORTH

#     def draw_cell(self, mlx: Any, mlx_ptr: Any,
#                   mlx_win: Any, event_handler: Any) -> None:
#         self._init(mlx, mlx_ptr, event_handler)
#         addr = mlx.mlx_get_data_addr(self.image.img)
#         self.image.data, self.image.bpp, self.image.sl, _ = addr
#         byte_per_pixel = self.image.bpp // 8
#         for j in range(self.height):
#             for i in range(self.width):
#                 offset = j * self.image.sl + i * byte_per_pixel
#                 self.image.data[offset:offset + byte_per_pixel] = CELL_COLOR.to_bytes(
#                         byte_per_pixel,
#                         'little')
#         if self.wall & NORTH:
#             for j in range(WALL_THICK):
#                 for i in range(self.width):
#                     offset = j * self.image.sl + i * byte_per_pixel
#                     self.image.data[offset:offset + byte_per_pixel] = WALL_COLOR.to_bytes(
#                             byte_per_pixel,
#                             'little'
#                             )
#         if self.wall & EAST:
#             for i in range(self.height):
#                 for j in range(WALL_THICK):
#                     offset = i * self.image.sl + j * byte_per_pixel
#                     self.image.data[offset:offset + byte_per_pixel] = WALL_COLOR.to_bytes(
#                             byte_per_pixel,
#                             'little'
#                             )
#         if self.wall & WEST:
#             for i in range(self.height):
#                 for j in range(WALL_THICK):
#                     offset = i * self.image.sl + j * byte_per_pixel
#                     self.image.data[offset:offset + byte_per_pixel] = WALL_COLOR.to_bytes(
#                             byte_per_pixel,
#                             'little'
#                             )
#         if self.wall & SOUTH:
#             for i in range(self.height):
#                 for j in range(WALL_THICK):
#                     offset = i * self.image.sl + j * byte_per_pixel
#                     self.image.data[offset:offset + byte_per_pixel] = WALL_COLOR.to_bytes(
#                             byte_per_pixel,
#                             'little'
#                             )
#         mlx.mlx_put_image_to_window(
#                 mlx_ptr, mlx_win, self.image.img,
#                 self.height * self.col, self.row * self.width)

#     def _init_wall(self, mlx: Any, mlx_ptr: Any) -> None:
#         if self.wall_initiated:
#             return None
#         self.wall_initiated = True
#         self.wall_img = Image()
#         self.wall_img.img = mlx.mlx_new_image(mlx_ptr, 5, 5)
