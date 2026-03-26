from src.setting import WEST
from ..cell import Cell

class Solver:
    def __init__(
        self, data: list[list[Cell]], 
        ENTRY: tuple[int, int], EXIT: tuple[int, int]
    ) -> None:
        self.data = data
        self.entry = ENTRY
        self.exit = EXIT
        self.path: list[tuple[int, int]] = []

    def dfs_solver(self, curr_pos: tuple[int, int]) -> bool:
        if curr_pos == self.exit:
            self.path.append(curr_pos)
            return True
        curr_x, curr_y = curr_pos
        curr_cell = self.data[curr_x][curr_y]
        curr_cell.is_visited = True
        negightboors = self.get_neightboor(curr_cell)
        for negightboor in negightboors:
            x, y = negightboor.row, negightboor.col
            if self.dfs_solver((x, y)):
                self.path.append((x, y))
                return True
        return False
