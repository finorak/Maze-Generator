from . import Maze
from mlx import Mlx
from typing import Any
from . import HEIGHT, WIDTH, TITLE
from . import Cell
from . import Image

class App:
    def __init__(self, config: Any) -> None:
        # self.maze = Maze(Mlx, "config.txt")
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()
        self.start = False
        self.main_win: Any = None
        self.maze_win: Any = None
        self.error_win: Any = None
        self.maze: Maze = Maze()
        self.config = config
        self.image = Image()

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
        else:
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
            "Appuyez sur une touche pour commencer..."
        )

        self.mlx.mlx_key_hook(self.main_win, self.on_key_main, None)
        self.mlx.mlx_hook(self.main_win, 33, 0, self.on_close, None)
    #----------------------main win---------------------------#

    #----------------------maze win---------------------------#
    def on_key_maze(self, key: Any, _param: Any) -> None:
        if key in (65307, ord('q')):
            self.mlx.mlx_loop_exit(self.ptr)

    def switch_to_maze(self) -> None:
        self.maze.init_data(self.config["width"], self.config["height"])

        if self.main_win is not None:
            self.mlx.mlx_destroy_window(self.ptr, self.main_win)
            self.main_win = None

        self.maze_win = self.mlx.mlx_new_window(
            self.ptr, WIDTH, HEIGHT, "Maze"
        )
        self.mlx.mlx_key_hook(self.maze_win, self.on_key_maze, None)
        self.mlx.mlx_hook(self.maze_win, 33, 0, self.on_close, None)

        self.start = True
    
    def draw_cell(self, cell: Cell):
        pass

    def draw_maze(self):
        pass
    #----------------------maze win---------------------------#