"""
The main program for our maze generator
"""

from src.setting import WIDTH, HEIGHT, TITLE
from mlx import Mlx


class Maze:
    """
    The maze class
    """
    def __init__(self) -> None:
        """
        Initialisation of our our maze
        """
        # we use this to see if the logo can be displayed
        self.show_logo = True
        # initializing mlx
        self._init()
        self.event_handler(self.mlx_window)
        self.mlx.mlx_loop(self.mlx_ptr)

    def _init(self):
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.mlx_window = self.mlx.mlx_new_window(
                self.mlx_ptr, WIDTH, HEIGHT, TITLE
                )

    def close(self, keycode: int = 33):
        """
        Closing the window
        :param keycode: the keycode we recieve from mlx_hook
        """
        # destroying the window
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.mlx_window)
        # exiting the mlx_loop
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def draw(self):
        """
        Drawing on the window and rendering
        """
        pass

    def update(self):
        """
        Updating the window
        """
        pass

    def event_handler(self, window):
        self.mlx.mlx_hook(window, 33, 0, self.close, None)


if __name__ == "__main__":
    maze = Maze()
