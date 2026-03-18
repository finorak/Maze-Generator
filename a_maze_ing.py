"""
The main program for our maze generator
"""

from typing import Any
from src.setting import WIDTH, HEIGHT, TITLE
from utils.utils import get_configuration
from mlx import Mlx


class Maze:
    """
    The maze class
    """
    ROWS = 20
    COLS = 15

    def __init__(self) -> None:
        """
        Initialisation of our our maze
        """
        # we use this to see if the logo can be displayed
        self.show_logo = True
        self.running = False
        self.config: None | dict = None

    def _init(self):
        self.config = get_configuration("config.txt")
        if self.config:
            self.running = True
            self.mlx = Mlx()
            self.mlx_ptr = self.mlx.mlx_init()
            self.mlx_window = self.mlx.mlx_new_window(
                self.mlx_ptr, WIDTH, HEIGHT, TITLE
                )

    def run(self):
        # initializing mlx
        self._init()
        if not self.running:
            return
        # rendering into window
        self.draw(self.mlx_window)
        # handling event
        self.event_handler(self.mlx_window)
        # looping over
        self.mlx.mlx_loop(self.mlx_ptr)

    def close_via_quit(self, keycode: int = 33):
        """
        Closing the window
        :param keycode: the keycode we recieve from mlx_hook
        """
        # destroying the window
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.mlx_window)
        # exiting the mlx_loop
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def draw_line(self, window: Any) -> None:
        """
        Drawing line into the window to give the vibe
        of a grid
        """
        if not self.config:
            return
        rows = self.config["width"]
        cols = self.config["height"]
        width_gap = HEIGHT // cols
        height_gap = WIDTH // rows
        for i in range(rows):
            for j in range(cols):
                pass

    def draw(self, window: Any):
        """
        Drawing on the window and rendering
        """
        self.draw_line(window)

    def update(self):
        """
        Updating the window
        """
        pass

    def handle_key(self, keycode: int) -> None:
        print(keycode)
        if keycode == 65307:
            self.close_via_quit(keycode)

    def event_handler(self, window: Any):
        """
        This function will contain all the event handler
        """
        self.mlx.mlx_hook(window, 3, 0, self.handle_key, None)
        self.mlx.mlx_hook(window, 33, 0,
                          self.close_via_quit, None)


if __name__ == "__main__":
    maze = Maze()
    maze.run()
