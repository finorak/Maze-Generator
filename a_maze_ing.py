"""
The main program for our maze generator
"""

from src.cell import Cell
from src.setting import WIDTH, HEIGHT, TITLE
from mlx import Mlx
from utils.utils import get_configuration

class Maze:
    """
    The maze class
    """
    def __init__(self) -> None:
        """
        Initialisation of our our maze
        """
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.mlx_window = self.mlx.mlx_new_window(
                self.mlx_ptr, WIDTH, HEIGHT, TITLE
                )
        self.mlx.mlx_loop(self.mlx_ptr)

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


if __name__ == "__main__":
    conf = get_configuration("config.txt")
    print(conf)
