from ..cell import Cell
from typing import Any
from ..setting import (
    NORTH,
    SOUTH,
    WEST,
    EAST,
    CELL_COLOR,
    DISPLAY_INTERVAL,
)
from collections import deque
from ..utils.color_genertor import rgb
from threading import Thread
from time import sleep


class Solver:
    def __init__(
        self,
        data: list[list[Cell]],
        ENTRY: tuple[int, int],
        EXIT: tuple[int, int],
        app: Any,
    ) -> None:
        self._data = data
        self.entry = ENTRY
        self.exit = EXIT
        self.path: list[tuple[int, int]] = []
        self.app = app
        self.is_generate = False
        self.found_path = False
        self.solver_threading: Any = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: list[list[Cell]]):
        self.is_generate = False
        self._data = data

    def dfs_solver(self, curr_pos: tuple[int, int]) -> None:
        def solve_maze(curr_pos: tuple[int, int]):
            if self.found_path:
                return True
            if curr_pos == self.exit:
                self.path.append(curr_pos)
                self.found_path = True
                return True
            curr_x, curr_y = curr_pos
            curr_cell = self.data[curr_x][curr_y]
            curr_cell.is_visited = True
            curr_cell.color = PATH_FOUND_COLOR
            self.app.draw_maze()
            directions = deque(self.find_directions(curr_cell))
            for direction in directions:
                _, new_x, new_y = direction
                if self.dfs_solver((new_x, new_y)):
                    self.path.append((new_x, new_y))
                    curr_cell.color = CLEAR_COLOR
                    self.app.draw_maze()
                    self.found_path = True
                    return True
                self.data[new_x][new_y].color = PATH_FOUND_COLOR
                self.app.draw_maze()
            self.app.draw_maze()
            return False

        solve_maze(curr_pos)
        self.is_generate = True

    def find_directions(self, cell: Cell) -> list[tuple[tuple[int, int], int, int]]:
        directions: list[tuple[tuple[int, int], int, int]] = []
        if cell.wall & NORTH == 0 and not self._data[cell.row][cell.col - 1].is_visited:
            directions.append(((cell.row, cell.col), cell.row, cell.col - 1))
        if cell.wall & EAST == 0 and not self._data[cell.row + 1][cell.col].is_visited:
            directions.append(((cell.row, cell.col), cell.row + 1, cell.col))
        if cell.wall & SOUTH == 0 and not self._data[cell.row][cell.col + 1].is_visited:
            directions.append(((cell.row, cell.col), cell.row, cell.col + 1))
        if cell.wall & WEST == 0 and not self._data[cell.row - 1][cell.col].is_visited:
            directions.append(((cell.row, cell.col), cell.row - 1, cell.col))
        return directions

    def solve(self) -> None:
        if self.is_generate:
            return
        self.path = []
        all_path: list[tuple[int, int]] = []
        x, y = self.entry
        self._data[x][y].is_visited = True
        directions = deque(self.find_directions(self._data[x][y]))
        while directions:
            direction = directions.popleft()
            parent, new_x, new_y = direction
            self._data[new_x][new_y].is_visited = True
            self._data[new_x][new_y].parent = parent
            if (new_x, new_y) == self.exit:
                break
            self._data[new_x][new_y].color = rgb(214, 106, 151)
            all_path.append((new_x, new_y))
            sleep(DISPLAY_INTERVAL)
            # self.app.draw_maze()
            directions.extend(self.find_directions(self._data[new_x][new_y]))

        x, y = self.exit
        while True:
            x_parent, y_parent = self._data[x][y].parent
            if (x_parent, y_parent) == self.entry:
                break
            self.path.append((x_parent, y_parent))
            self._data[x_parent][y_parent].color = rgb(106, 214, 205)
            sleep(DISPLAY_INTERVAL)
            # self.app.draw_maze()
            x, y = self._data[x][y].parent
        self.path.reverse()
        for p in all_path:
            x, y = p
            self._data[x][y].color = CELL_COLOR
        for p in self.path:
            x, y = p
            self._data[x][y].color = rgb(106, 214, 205)
        sleep(DISPLAY_INTERVAL)
        # self.app.draw_maze()
        self.is_generate = True

    def start_solve(self, target: Any, args: Any):
        if self.solver_threading is not None and self.solver_threading.is_alive():
            print("solve in progress...")
            return
        self.solver_threading = Thread(target=target, args=args)
        self.solver_threading.daemon = True
        self.solver_threading.start()
