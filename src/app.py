from time import time
from .maze import Maze
from mlx import Mlx
from typing import Any
from .setting import (
    HEIGHT,
    HELP_HEIGHT,
    HELP_WIDTH,
    STRING_HEIGHT_PADDDING,
    STRING_WIDTH_PADDING,
    WIDTH,
    TITLE,
    NORTH,
    SOUTH,
    WEST,
    EAST,
    WALL_THICK,
    WALL_COLOR,
    DISPLAY_INTERVAL,
    CELL_SIZE
)
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
        self.help_win: Any = None
        self.config = config
        self.output_file = self.config.get("output_file")
        self.maze: Maze = Maze(self)
        self.rows = config.get("height")
        self.cols = config.get("width")
        self.maze.init_data(self.rows, self.cols)
        self.solver: Solver = Solver(
            self.maze.data, self.maze.entry_pos, self.maze.end_pos, self
        )
        self.last_draw: float = 0

    def init_image(self) -> None:
        if self.maze.data and self.maze.data[0][0].image.img is None:
            for row in self.maze.data:
                for cell in row:
                    if cell.image.img is None:
                        cell.image.img = self.mlx.mlx_new_image(
                            self.ptr, cell.size, cell.size
                        )

    def on_close(self, _param: Any) -> None:
        self.mlx.mlx_loop_exit(self.ptr)

    def on_close_help(self, _param: Any) -> None:
        if self.help_win is not None:
            self.mlx.mlx_destroy_window(self.ptr, self.help_win)
            self.help_win = None

    def draw_help_win(self) -> None:
        if self.help_win is None:
            return None

        lines = [
            "Help / Controls",
            "",
            "Space : open the maze screen",
            "g     : generate the maze",
            "s     : solve with A*",
            "d     : solve with DFS",
            "c     : save the maze",
            "r     : reset the maze",
            "h     : open this help window",
            "q/Esc : quit the application",
        ]

        y = 20
        for index, text in enumerate(lines):
            color = 0xFFFFFFFF if index == 0 else 0xFFD0D0D0
            self.mlx.mlx_string_put(
                self.ptr,
                self.help_win,
                20,
                y,
                color,
                text,
            )
            y += 22

    def open_help_window(self) -> None:
        if self.help_win is not None:
            return None

        self.help_win = self.mlx.mlx_new_window(
            self.ptr,
            HELP_WIDTH,
            HELP_HEIGHT,
            "Help",
        )
        self.draw_help_win()
        self.mlx.mlx_key_hook(self.help_win, self.on_key_help, None)
        self.mlx.mlx_hook(self.help_win, 33, 0, self.on_close_help, None)

    def on_key_help(self, key: Any, _param: Any) -> None:
        if key in (65307, ord("q")):
            self.mlx.mlx_loop_exit(self.ptr)

    def update(self, _param: Any) -> None:
        if self.start:
            now = time()
            if now - self.last_draw >= DISPLAY_INTERVAL:
                self.draw_maze()
                self.last_draw = now

    def run(self) -> None:
        self.run_main()
        self.mlx.mlx_loop_hook(self.ptr, self.update, None)
        self.mlx.mlx_loop(self.ptr)
        if self.main_win is not None:
            self.mlx.mlx_destroy_window(self.ptr, self.main_win)
        if self.maze_win is not None:
            self.mlx.mlx_destroy_window(self.ptr, self.maze_win)
        if self.error_win is not None:
            self.mlx.mlx_destroy_window(self.ptr, self.error_win)
        if self.help_win is not None:
            self.mlx.mlx_destroy_window(self.ptr, self.help_win)
        self.mlx.mlx_release(self.ptr)

    # ----------------------main win---------------------------#
    def on_key_main(self, key: Any, _param: Any) -> None:
        if key in (65307, ord("q")):
            self.mlx.mlx_loop_exit(self.ptr)
        elif key == 32:
            self.switch_to_maze()
        elif key == ord("h"):
            self.open_help_window()

    def run_main(self) -> None:
        self.main_win = self.mlx.mlx_new_window(self.ptr, WIDTH, HEIGHT, TITLE)
        self.mlx.mlx_string_put(
            self.ptr,
            self.main_win,
            WIDTH // 2 - STRING_WIDTH_PADDING,
            STRING_HEIGHT_PADDDING,
            0xFFFFFFFF,
            "Choose options:",
        )

        self.mlx.mlx_key_hook(self.main_win, self.on_key_main, None)
        self.mlx.mlx_hook(self.main_win, 33, 0, self.on_close, None)

    # ----------------------main win---------------------------#

    # ----------------------maze win---------------------------#
    def on_key_maze(self, key: Any, _param: Any) -> None:
        a_star = self.solver.solve
        dfs = self.solver.dfs_solver
        if key in (65307, ord("q")):
            self.mlx.mlx_loop_exit(self.ptr)
        elif key == ord("g"):
            if self.maze.is_generate:
                return None
            self.maze.start_generate()
            self.solver.data = self.maze.data
        elif key == ord("s"):
            if self.maze.is_generate:
                self.solver.start_solve(a_star, ())
            else:
                print("maze not generate")
        elif key == ord("d"):
            if self.maze.is_generate:
                self.solver.start_solve(dfs, (self.solver.entry,))
            else:
                print("maze not generate")
        elif key == ord("c"):
            print("nothing")
        elif key == ord('h'):
            self.open_help_window()
        elif key == ord("r"):
            self.reinitialise()

    def reinitialise(self) -> None:
        if not self.maze.is_generate and not self.solver.found_path:
            return None
        self.maze.init_data(self.rows, self.cols)
        self.solver.found_path = False
        self.solver.solver_threading = None
        self.solver.path.clear()
        self.draw_maze()

    def switch_to_maze(self) -> None:
        if self.main_win is not None:
            self.mlx.mlx_destroy_window(self.ptr, self.main_win)

        self.width = self.config.get("width") * CELL_SIZE
        self.height = self.config.get("height") * CELL_SIZE
        self.maze_win = self.mlx.mlx_new_window(
                self.ptr, self.width, self.height, TITLE
                )
        self.draw_maze()
        self.draw_maze()
        self.event_handler()

        self.start = True

    def mouse_handler(self, button: Any, x: int, y: int, _param: Any) -> None:
        """
        Setting the position of entry and exit
        """
        row = (y * 40) // self.height
        col = (x * 40) // self.width
        print(button, (row, self.height), (col, self.width))

    def event_handler(self) -> None:
        self.mlx.mlx_mouse_hook(self.maze_win, self.mouse_handler, None)
        self.mlx.mlx_hook(self.maze_win, 33, 0, self.on_close, None)
        self.mlx.mlx_key_hook(self.maze_win, self.on_key_maze, None)

    def draw_cell(self, cell: Cell):
        addr = self.mlx.mlx_get_data_addr(cell.image.img)
        cell.image.data, cell.image.bpp, cell.image.sl, _ = addr
        bpp = cell.image.bpp // 8
        for j in range(cell.size):
            for i in range(cell.size):
                offset = j * cell.image.sl + i * bpp
                cell.image.data[offset:offset + bpp] = cell.color.to_bytes(
                    bpp, "little"
                )

        if cell.wall & NORTH:
            for j in range(WALL_THICK):
                for i in range(cell.size):
                    offset = (j) * cell.image.sl + (i) * bpp
                    cell.image.data[offset:offset + bpp] = WALL_COLOR.to_bytes(
                        bpp, "little"
                    )
        if cell.wall & EAST:
            for j in range(cell.size):
                for i in range(WALL_THICK):
                    offset = j * cell.image.sl + (cell.size - 1) * bpp
                    cell.image.data[offset:offset + bpp] = WALL_COLOR.to_bytes(
                        bpp, "little"
                    )
        if cell.wall & WEST:
            for j in range(cell.size):
                for i in range(WALL_THICK):
                    offset = j * cell.image.sl + i * bpp
                    cell.image.data[offset:offset + bpp] = WALL_COLOR.to_bytes(
                        bpp, "little"
                    )
        if cell.wall & SOUTH:
            for j in range(WALL_THICK):
                for i in range(cell.size):
                    offset = (cell.size - 1) * cell.image.sl + (i) * bpp
                    cell.image.data[offset:offset + bpp] = WALL_COLOR.to_bytes(
                        bpp, "little"
                    )
        self.mlx.mlx_put_image_to_window(
            self.ptr,
            self.maze_win,
            cell.image.img,
            cell.row * cell.size,
            cell.col * cell.size,
        )

    def draw_maze(self) -> None:
        self.init_image()
        for row in self.maze.data:
            for cell in row:
                self.draw_cell(cell)
