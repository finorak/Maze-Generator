from random import shuffle
from typing import Any

from src.setting import CELL_COLOR, VISITED_COLOR
from ..cell import Cell


class Solver:
    def __init__(self, data: list[list[Cell]]) -> None:
        self.data = data
        self.result = {}

    def dfs_solver(self, curr_pos: tuple[int, int],
                   end_pos: tuple[int, int],
                   draw_func: Any) -> bool:
        if curr_pos == end_pos:
            return True
        curr_x, curr_y = curr_pos
        cell = self.data[curr_x][curr_y]
        cell.is_visited = True
        cell.color = VISITED_COLOR
        draw_func()
        negithboors = cell.get_neightboors(self.data) or []
        if negithboors:
            shuffle(negithboors)
        for negithboor in negithboors:
            if negithboor.is_visited:
                continue
            x, y = negithboor.row, negithboor.col
            if self.dfs_solver((x, y), end_pos, draw_func):
                return True
            self.data[x][y].color = CELL_COLOR
        return False
