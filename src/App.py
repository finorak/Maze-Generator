from .Maze import Maze
from mlx import Mlx
from typing import Any
from .setting import (HEIGHT, WIDTH, TITLE, NORTH, SOUTH,
                      WEST, EAST, WALL_THICK, WALL_COLOR,
                      CELL_COLOR, BLOCK_42_COLOR)
from .Cell import Cell


class App:
    def __init__(self, config: Any) -> None:
        # self.maze = Maze(Mlx, "config.txt")
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()
        self.start = False
        self.main_win: Any = None
        self.maze_win: Any = None
        self.error_win: Any = None
        self.config = config
        self.maze: Maze = Maze(self)
        self.counter = 0
        # self.image = Image()
        self.maze.init_data(config.get("height"), config.get("width"))

    def init_image(self):
        if self.maze.data[0][0].image.img is None:
            for i in range(len(self.maze.data)):
                for j in range(len(self.maze.data[i])):
                    if self.maze.data[i][j].image.img is None:
                        self.maze.data[i][j].image.img = self.mlx.mlx_new_image(
                            self.ptr,
                            self.maze.data[i][j].size,
                            self.maze.data[i][j].size
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
            WIDTH // 2 - 200,
            HEIGHT // 2,
            0xFFFFFF,
            "Appuyez sur espace pour commencer..."
        )

        self.mlx.mlx_key_hook(self.main_win, self.on_key_main, None)
        self.mlx.mlx_hook(self.main_win, 33, 0, self.on_close, None)
    #----------------------main win---------------------------#

    #----------------------maze win---------------------------#
    def on_key_maze(self, key: Any, _param: Any) -> None:
        if key in (65307, ord('q')):
            self.mlx.mlx_loop_exit(self.ptr)
        elif key == ord('s'):
            self.maze.generete()

    def switch_to_maze(self) -> None:
        if self.main_win is not None:
            self.mlx.mlx_destroy_window(self.ptr, self.main_win)
            self.main_win = None

        self.maze_win = self.mlx.mlx_new_window(
            self.ptr, WIDTH, HEIGHT, TITLE
        )
        self.draw_maze()
        self.mlx.mlx_key_hook(self.maze_win, self.on_key_maze, None)
        self.mlx.mlx_hook(self.maze_win, 33, 0, self.on_close, None)

        self.start = True

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
                    offset = j * cell.image.sl + (cell.size - i - 1) * byte_per_pixel
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
                    offset = (cell.size - j - 1) * cell.image.sl + (i) * byte_per_pixel
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
