from time import time

from src.engine.navigator import PlayerNavigator
from .maze import Maze
from mlx import Mlx
import pygame
from typing import Any
from .setting import (
    HEIGHT,
    HELP_HEIGHT,
    HELP_TEXT,
    HELP_WIDTH,
    WALL_COLORS,
    WIDTH,
    TITLE,
    DISPLAY_INTERVAL,
    CELL_SIZE,
    IMAGES,
    get_path,
)
from .cell import Cell
from .engine.solver import Solver
from src.utils.maze_utils import put_maze_into_file
import os
from .image import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class App:
    def __init__(self, config: dict[str, Any]) -> None:
        pygame.init()
        self.mlx = Mlx()
        self.ptr = self.mlx.mlx_init()
        self.start = False
        self.init_attribute(config)
        self.navigator = PlayerNavigator(self)

    def init_attribute(self, config: Any) -> None:
        self.main_win: Any = None
        self.maze_win: Any = None
        self.error_win: Any = None
        self.help_win: Any = None
        self.config = config
        self.rows = self.config.get("height")
        self.cols = self.config.get("width")
        self.entry_pos: tuple[int, int] | Any = self.config.get('entry')
        self.end_pos: tuple[int, int] | Any = self.config.get('exit')
        self.perfect: bool = self.config.get('perfect')
        if self.perfect is None:
            self.perfect = True
        self.maze: Maze = Maze(self.entry_pos,
                               self.end_pos, self.rows,
                               self.cols, self.perfect)
        self.maze.init_data()
        self.solver: Solver = Solver(
            self.maze.data, self.entry_pos, self.end_pos
        )
        self.index = 0
        self.wall_color = WALL_COLORS[self.index % len(WALL_COLORS)]
        self.last_draw: float = 0
        self.images: dict[str, Any] = {}
        self.get_image()
        self.bg = Image()
        self.load_sound_effect()

    def load_sound_effect(self) -> None:
        self.playing = False
        self.game_start = pygame.mixer.Sound(
                get_path(BASE_DIR, "game_start.mp3")
                )
        self.end_reached = pygame.mixer.Sound(
                get_path(BASE_DIR, "end_reached.mp3")
                )
        self.troll_sound = pygame.mixer.Sound(
                get_path(BASE_DIR, "fah.mp3")
                    )
        self.found_sound = pygame.mixer.Sound(
                get_path(BASE_DIR, "path_found_vfx.mp3")
                )
        self.game_start.play()

    def init_image(self) -> None:
        if not self.maze.data:
            return None
        if self.maze.data[0][0].image.img is not None:
            return None
        for row in self.maze.data:
            for cell in row:
                if cell.image.img is None:
                    cell.image.img = self.mlx.mlx_new_image(
                        self.ptr, cell.size, cell.size
                    )

    def get_image(self) -> None:
        for key, value in IMAGES.items():
            path = os.path.normpath(
                os.path.join(BASE_DIR, "..", *(value.split('/')))
            )
            img, _, _ = self.mlx.mlx_png_file_to_image(self.ptr, path)
            self.images.update({key: img})

    def on_close(self, _param: Any) -> None:
        self.mlx.mlx_loop_exit(self.ptr)

    def on_close_help(self, _param: Any) -> None:
        if self.help_win is not None:
            self.mlx.mlx_destroy_window(self.ptr, self.help_win)
            self.help_win = None

    def draw_help_win(self) -> None:
        if self.help_win is None:
            return None

        y = 20
        for index, text in enumerate(HELP_TEXT):
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
            pygame.mixer.music.stop()
        elif key == ord('o'):
            self.mlx.mlx_destroy_image(self.ptr, self.images.get("home"))
        elif key == 32:
            self.switch_to_maze()
            self.troll_sound.stop()
        elif key == ord("h"):
            self.open_help_window()

    def get_wall_color(self) -> int:
        return self.wall_color

    def run_main(self) -> None:
        self.main_win = self.mlx.mlx_new_window(self.ptr, WIDTH, HEIGHT, TITLE)
        self.draw_image(self.main_win, (0, 0), self.images.get("home"))
        self.mlx.mlx_key_hook(self.main_win, self.on_key_main, None)
        self.mlx.mlx_hook(self.main_win, 33, 0, self.on_close, None)

    def on_key_maze(self, key: Any, _param: Any) -> None:
        a_star = self.solver.solve
        dfs = self.solver.dfs_solver
        if key in (65307, ord("q")):
            self.mlx.mlx_loop_exit(self.ptr)
        elif key == ord("g"):
            if self.maze.is_generate:
                self.troll_sound.play()
                print("Maze already generated")
                return None
            if self.entry_pos == self.end_pos:
                self.entry_pos = (0, 0)
                self.end_pos = (self.cols - 1, self.rows - 1)
                self.maze.entry_pos = (0, 0)
                self.maze.end_pos = self.end_pos
                self.solver.entry = self.entry_pos
                self.solver.exit = self.end_pos
            self.maze.start_generate()
            self.solver.data = self.maze.data
            self.activate_mouse = False
        elif key == ord("s"):
            if self.maze.is_generate:
                self.activate_mouse = False
                self.solver.start_solve(
                        a_star,
                        (lambda: self.get_wall_color(),
                         self.maze.change_color))
                self.playing = True
            else:
                self.troll_sound.play()
                print("maze not generate")
        elif key == ord("d"):
            if self.maze.is_generate:
                self.playing = True
                self.activate_mouse = False
                self.solver.start_solve(dfs, (lambda: self.get_wall_color(),
                                              self.maze.change_color,
                                              self.entry_pos,))
            else:
                self.troll_sound.play()
                print("maze not generate")
        elif key == ord("w"):
            if self.thread_running() or not self.solver.found_path:
                print("Can't write maze to file")
                self.troll_sound.play()
                return None
            self.activate_mouse = False
            put_maze_into_file(
                    self.config.get('output_file'),
                    self.maze.data,
                    self.solver.path,
                    self.entry_pos,
                    self.end_pos)
        elif key == ord('h'):
            self.open_help_window()
        elif key == ord('c'):
            self.index = (self.index + 1) % len(WALL_COLORS)
            self.wall_color = WALL_COLORS[self.index]
            if (
                    self.solver.solver_threading is not None
                    and self.solver.solver_threading.is_alive()
            ):
                self.maze.change_color(self.wall_color, "solve")
            else:
                self.maze.change_color(self.wall_color, "all")
        elif key == ord("r"):
            if (
                    self.solver.solver_threading is not None
                    and self.solver.solver_threading.is_alive()
            ):
                print("Can't regenerate, wait...")
                self.troll_sound.play()
                return None
            self.reinitialise(
                    show_logo=self.maze.show_logo,
                    perfect=self.perfect)
        elif key == ord('p'):
            if (
                    self.solver.solver_threading is not None
                    and self.solver.solver_threading.is_alive()
            ):
                print("Can't regenerate, wait...")
                self.troll_sound.play()
                return None
            self.perfect = not self.perfect
            self.maze.perfect = self.perfect
            self.reinitialise(
                    show_logo=self.maze.show_logo,
                    perfect=self.perfect)
        elif key == ord("f"):
            if (
                    self.solver.solver_threading is not None
                    and self.solver.solver_threading.is_alive()
            ):
                print("Can't regenerate, wait...")
                self.troll_sound.play()
                return None
            self.maze.perfect = self.perfect
            self.maze.show_logo = not self.maze.show_logo
            if self.maze.show_logo:
                if self.entry_pos in self.maze.block:
                    self.entry_pos = (0, 0)
                if self.end_pos in self.maze.block:
                    self.end_pos = (self.cols - 1, self.rows - 1)
            self.maze.entry_pos = self.entry_pos
            self.maze.end_pos = self.end_pos
            self.solver.entry = self.entry_pos
            self.solver.exit = self.end_pos
            self.reinitialise(
                    show_logo=self.maze.show_logo,
                    perfect=self.perfect)

    def thread_running(self) -> bool:
        return (
            self.solver.solver_threading is not None
            and self.solver.solver_threading.is_alive()
        )

    def reinitialise(self,
                     show_logo: bool | None = True,
                     perfect: bool = True) -> None:
        if not self.maze.is_generate and not self.solver.found_path:
            return None
        self.navigator.can_move = False
        self.maze.perfect = perfect
        self.maze.show_logo = show_logo
        self.maze.init_data()
        self.maze.change_color(self.get_wall_color(), "all")
        self.solver.is_generate = False
        self.solver.found_path = False
        self.solver.solver_threading = None
        self.solver.path.clear()
        self.solver.remove_color = True

    def switch_to_maze(self) -> None:
        if self.main_win is not None:
            self.mlx.mlx_destroy_window(self.ptr, self.main_win)

        self.width = self.config.get("width") * CELL_SIZE
        self.height = self.config.get("height") * CELL_SIZE
        self.maze_win = self.mlx.mlx_new_window(
                self.ptr, self.width, self.height, TITLE
                )
        self.init_image()
        self.draw_maze(True)
        self.draw_maze(True)
        self.event_handler()

        self.start = True

    def mouse_handler(self, button: Any, x: int, y: int, _param: Any) -> None:
        """
        Setting the position of entry and exit
        """
        if button != 1 and button != 3:
            print("Button not reconized")
            return
        if not self.maze.is_generate:
            print("maze not generate")
            return
        if self.thread_running():
            print("Solver running can't modify maze")
            return
        row = (x // CELL_SIZE)
        col = (y // CELL_SIZE)
        if button == 1:
            x_entry, y_entry = self.entry_pos
            if (
                (row, col) == self.end_pos or
                self.maze.data[row][col].is_42_cell
            ):
                return
            self.maze.data[x_entry][y_entry].updated = False
            self.entry_pos = (row, col)
            self.maze.entry_pos = (row, col)
            self.solver.entry = (row, col)
            self.navigator.x = row
            self.navigator.y = col
        if button == 3:
            x_end, y_end = self.end_pos
            if (
                (row, col) == self.entry_pos or
                self.maze.data[row][col].is_42_cell
            ):
                return
            self.maze.data[x_end][y_end].updated = False
            self.end_pos = (row, col)
            self.maze.end_pos = (row, col)
            self.solver.exit = (row, col)

    def event_handler(self) -> None:
        self.mlx.mlx_hook(self.maze_win, 2, 1, self.navigator.move, None)
        self.mlx.mlx_mouse_hook(self.maze_win, self.mouse_handler, None)
        self.mlx.mlx_key_hook(self.maze_win, self.on_key_maze, None)
        self.mlx.mlx_hook(self.maze_win, 33, 0, self.on_close, None)

    def draw_backgroud(self) -> None:
        self.mlx.mlx_put_image_to_window(
            self.ptr, self.maze_win, self.bg.img,
            0, 0
        )

    def draw_image(self, win: Any, pos: tuple[int, int], img: Any) -> None:
        self.mlx.mlx_put_image_to_window(
            self.ptr,
            win,
            img,
            *pos
        )

    def draw_cell(self, cell: Cell, update_all: bool = False) -> None:
        pos = (cell.row * cell.size, cell.col * cell.size)
        if not cell.updated or update_all:
            addr = self.mlx.mlx_get_data_addr(cell.image.img)
            cell.image.data, cell.image.bpp, cell.image.sl, _ = addr
            bpp = cell.image.bpp // 8
            for j in range(cell.size):
                for i in range(cell.size):
                    offset = j * cell.image.sl + i * bpp
                    cell.image.data[offset:offset + bpp] = cell.color.to_bytes(
                        bpp, "little"
                    )
            self.draw_image(self.maze_win, pos, cell.image.img)
            cell.updated = True
            self.draw_image(
                self.maze_win, pos, self.images.get(f"{cell.wall:04b}")
            )
        if self.maze.is_generate and (cell.row, cell.col) == self.entry_pos:
            self.draw_image(
                self.maze_win, (pos[0] + 3, pos[1] + 3),
                self.images.get("entry")
            )
        if self.maze.is_generate and (cell.row, cell.col) == self.end_pos:
            self.draw_image(
                self.maze_win, (pos[0] + 12, pos[1] + 5),
                self.images.get("exit")
            )
        if self.maze.is_generate and (cell.row, cell.col) in self.solver.path:
            self.draw_image(
                    self.maze_win,
                    pos,
                    self.images.get("path"))
        if not self.maze.is_generate and \
                (cell.row, cell.col) == self.maze.wall_destroyer:
            self.draw_image(
                    self.maze_win,
                    pos,
                    self.images.get("path"))
            cell.updated = False

    def draw_maze(self, update_all: bool = False) -> None:
        for row in self.maze.data:
            for cell in row:
                self.draw_cell(cell, update_all)
