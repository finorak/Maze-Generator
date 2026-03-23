"""
The main program for our maze generator
"""


from mlx import Mlx
from src.Maze import Maze


class App:
    def __init__(self) -> None:
        self.maze = Maze(Mlx)

    def run(self) -> None:
        self.maze.generate("config.txt")


if __name__ == "__main__":
    app = App()
    app.run()
