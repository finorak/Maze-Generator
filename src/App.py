from . import Maze
from mlx import Mlx

class App:
    def __init__(self) -> None:
        self.maze = Maze(Mlx, "config.txt")

    def run(self) -> None:
        self.maze.generate()