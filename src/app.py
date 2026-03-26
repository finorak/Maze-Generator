from .maze import Maze
from mlx import Mlx
from typing import Any
from .setting import (HEIGHT, STRING_HEIGHT_PADDDING,
                      STRING_WIDTH_PADDING, WIDTH,
                      TITLE, NORTH, SOUTH, WEST,
                      EAST, WALL_THICK, WALL_COLOR)
from .cell import Cell
from .engine.solver import Solver


class App:
    def __init__(self, config: Any) -> None:
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()
        self.start = False
        self.main_win: Any = None
        self.maze_win: Any = None
        self.error_win: Any = None
        self.config = config
        self.maze: Maze = Maze(self)
        self.counter = 0
        self.maze.init_data(config.get("height"), config.get("width"))
        self.solver: Solver = Solver(self.maze.data, self.maze.entry_pos, self.maze.end_pos, self)

    def init_image(self):
        if self.maze.data and self.maze.data[0][0].image.img is None:
            for row in self.maze.data:
                for cell in row:
                    if cell.image.img is None:
                        cell.image.img = self.mlx.mlx_new_image(
                            self.ptr,
                            cell.size,
                            cell.size
                        )

    def on_close(self, _param: Any) -> None:
        self.mlx.mlx_loop_exit(self.ptr)

    def update(self, _param: Any):
        pass

    def run(self):
        self.run_main()
        self.mlx.mlx_loop_hook(self.ptr, self.update, None)
        self.mlx.mlx_loop(self.ptr)
        if self.main_win is not None:
            self.mlx.mlx_destroy_window(self.ptr, self.main_win)
        if self.maze_win is not None:
            self.mlx.mlx_destroy_window(self.ptr, self.maze_win)
        if self.error_win is not None:
            self.mlx.mlx_destroy_window(self.ptr, self.error_win)
        self.mlx.mlx_release(self.ptr)

    #----------------------main win---------------------------#
    def on_key_main(self, key: Any, _param: Any) -> None:
        if key in (65307, ord('q')):
            self.mlx.mlx_loop_exit(self.ptr)
        elif key == 32:
            self.switch_to_maze()

    def run_main(self) -> None:
        self.main_win = self.mlx.mlx_new_window(
            self.ptr, WIDTH, HEIGHT, TITLE
        )
        self.mlx.mlx_string_put(
            self.ptr, self.main_win,
            WIDTH // 2 - STRING_WIDTH_PADDING,
            STRING_HEIGHT_PADDDING,
            0xFFFFFFFF,
            "Choose options:"
        )

        self.mlx.mlx_key_hook(self.main_win, self.on_key_main, None)
        self.mlx.mlx_hook(self.main_win, 33, 0, self.on_close, None)
    #----------------------main win---------------------------#

    #----------------------maze win---------------------------#
    def on_key_maze(self, key: Any, _param: Any) -> None:
        if key in (65307, ord('q')):
            self.mlx.mlx_loop_exit(self.ptr)
        elif key == ord('g'):
            self.maze.generete()
            self.solver.data = self.maze.data
        elif key == ord('s'):
            if not self.maze.is_generate:
                self.maze.generete()
                self.maze.is_generate = True
            else:
                self.solver.dfs_solver(self.maze.entry_pos)
        elif key == ord('c'):
            self.reinitialise()

    def reinitialise(self):
        pass

    def switch_to_maze(self) -> None:
        if self.main_win is not None:
            self.mlx.mlx_destroy_window(self.ptr, self.main_win)
            self.main_win = None

        self.maze_win = self.mlx.mlx_new_window(
            self.ptr, WIDTH, HEIGHT, TITLE
        )
        self.draw_maze()
        self.draw_maze()
        self.event_handler()

        self.start = True

    def mouse_handler(self, button: Any, x: int, y: int, _param: Any) -> None:
        """
        Setting the position of entry and exit
        """
        row = x // self.maze.cols
        col = y // self.maze.height
        print(button, (row, self.maze.cols), (col, self.maze.height))

    def event_handler(self):
        self.mlx.mlx_mouse_hook(self.maze_win, self.mouse_handler, None)
        self.mlx.mlx_hook(self.maze_win, 33, 0, self.on_close, None)
        self.mlx.mlx_key_hook(self.maze_win, self.on_key_maze, None)

    def draw_cell(self, cell: Cell):
        addr = self.mlx.mlx_get_data_addr(cell.image.img)
        cell.image.data, cell.image.bpp, cell.image.sl, _ = addr
        byte_per_pixel = cell.image.bpp // 8
        for j in range(cell.size):
            for i in range(cell.size):
                offset = j * cell.image.sl + i * byte_per_pixel
                cell.image.data[offset:offset + byte_per_pixel] = cell.color.to_bytes(
                        byte_per_pixel,
                        'little')

        if cell.wall & NORTH:
            for j in range(WALL_THICK):
                for i in range(cell.size):
                    offset = (j) * cell.image.sl + (i) * byte_per_pixel
                    cell.image.data[offset:offset + byte_per_pixel] = WALL_COLOR.to_bytes(
                            byte_per_pixel,
                            'little'
                            )
        if cell.wall & EAST:
            for j in range(cell.size):
                for i in range(WALL_THICK):
                    offset = j * cell.image.sl + (cell.size - 1) * byte_per_pixel
                    cell.image.data[offset:offset + byte_per_pixel] = WALL_COLOR.to_bytes(
                            byte_per_pixel,
                            'little'
                            )
        if cell.wall & WEST: 
            for j in range(cell.size):
                for i in range(WALL_THICK):
                    offset = j * cell.image.sl + i * byte_per_pixel
                    cell.image.data[offset:offset + byte_per_pixel] = WALL_COLOR.to_bytes(
                            byte_per_pixel,
                            'little'
                            )
        if cell.wall & SOUTH:
            for j in range(WALL_THICK):
                for i in range(cell.size):
                    offset = (cell.size - 1) * cell.image.sl + (i) * byte_per_pixel
                    cell.image.data[offset:offset + byte_per_pixel] = WALL_COLOR.to_bytes(
                            byte_per_pixel,
                            'little'
                            )
        self.mlx.mlx_put_image_to_window(
            self.ptr, self.maze_win, cell.image.img,
            cell.row * cell.size,cell.col * cell.size
        )

    def draw_maze(self):
        self.init_image()
        for row in self.maze.data:
            for cell in row:
                self.draw_cell(cell)
