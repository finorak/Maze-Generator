from typing import Any
from .Cell import Cell
from . import DIRECTIONS
from random import shuffle


class Maze:
    def __init__(self, parent: Any):
        self.data: list[list[Cell]] | Any = None
        self.rows = 0
        self.cols = 0
        self.parent = parent
        self.perfect = parent.config.get("perferct")

    def init_data(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.data = [
            [
                Cell(i, j) for j in range(self.rows)
            ] for i in range(self.cols)
        ]
        self.make_42_block()

    def make_42_block(self):
        def set_four(x: int, y: int) -> None:
            for i in range(3):
                self.data[x][y + i].is_42_cell = True
                self.data[x + 2][y + 2 + i].is_42_cell = True
            self.data[x + 1][y + 2].is_42_cell = True

        def set_two(x: int, y: int) -> None:
            for i in range(3):
                self.data[x + i][y].is_42_cell = True
                self.data[x + i][y + 2].is_42_cell = True
                self.data[x + i][y + 4].is_42_cell = True
            self.data[x + 2][y + 1].is_42_cell = True
            self.data[x][y + 3].is_42_cell = True

        set_four(self.cols//2 - 3, self.rows//2 - 2)
        set_two(self.cols//2 + 1, self.rows//2 - 2)

    def generete(self):
        entry_pos = self.parent.config.get('entry')
        end_pos = self.parent.config.get('exit')
        if self.perfect:
            self.generate_perfect_mage()
        else:
            self.generate_non_perfect_mage(entry_pos, entry_pos, end_pos)

    def generate_perfect_mage(self) -> None:
        pass

    def generate_non_perfect_mage(self, current_pos: tuple[int, int],
                                  start_pos: tuple[int, int],
                                  end_pos: tuple[int, int]) -> None:
        pass
