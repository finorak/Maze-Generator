from ..cell import Cell
from typing import Any

class Solver:
    def __init__(
        self, data: list[list[Cell]], 
        ENTRY: tuple[int, int], EXIT: tuple[int, int]
    ) -> None:
        self.data = data
        self.entry = ENTRY
        self.exit = EXIT
        self.path: list[tuple[int, int]] = []

    def dfs_solver(self, param) -> None:
        pass

