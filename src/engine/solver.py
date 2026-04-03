from ..cell import Cell
from typing import Any
from ..setting import (
    CELL_SIZE,
    NORTH,
    SOUTH,
    WEST,
    EAST,
    CELL_COLOR,
    DISPLAY_INTERVAL,
    PATH_FOUND_COLOR,
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
        self.solver_threading: Thread | Any = None

    @property
    def data(self) -> list[list[Cell]]:
        return self._data

    @data.setter
    def data(self, data: list[list[Cell]]) -> None:
        self.is_generate = False
        self._data = data

    def dfs_solver(self, curr_pos: tuple[int, int]) -> None:
        if self.found_path:
            return None

        def solve_maze(curr_pos: tuple[int, int]) -> bool:
            if self.found_path:
                print("hello")
                return True
            if curr_pos == self.exit:
                self.found_path = True
                return True
            curr_x, curr_y = curr_pos
            curr_cell = self.data[curr_x][curr_y]
            curr_cell.is_visited = True
            curr_cell.color = PATH_FOUND_COLOR
            sleep(DISPLAY_INTERVAL)
            directions = deque(self.find_directions(curr_cell))
            for direction in directions:
                if self.found_path or self.solver_threading is None:
                    return True
                parent, new_x, new_y = direction
                if (
                        self._data[new_x][new_y].is_42_cell
                        or self._data[new_x][new_y].is_visited
                ):
                    continue
                self.data[new_x][new_y].parent = parent
                if self.dfs_solver((new_x, new_y)):
                    self.path.append((new_x, new_y))
                    curr_cell.color = PATH_FOUND_COLOR
                    sleep(DISPLAY_INTERVAL)
                    self.path.append((new_x, new_y))
                    self.found_path = True
                    return True
                if not self.found_path:
                    self.data[new_x][new_y].color = CELL_COLOR
                else:
                    self.data[new_x][new_y].col = rgb(255, 0, 0)
                sleep(DISPLAY_INTERVAL)
            sleep(DISPLAY_INTERVAL)
            return False

        solve_maze(curr_pos)
        self.is_generate = True

    def find_directions(self,
                        cell: Cell
                        ) -> list[tuple[tuple[int, int], int, int]]:
        directions: list[tuple[tuple[int, int], int, int]] = []
        if cell.is_42_cell:
            return []
        x, y = cell.row, cell.col
        if (
                cell.wall & NORTH == 0
                and not self._data[x][y - 1].is_visited
                and not self.data[x][y - 1].is_42_cell
        ):
            directions.append(((x, y), x, y - 1))
        if (
                cell.wall & EAST == 0
                and not self._data[x + 1][y].is_visited
                and not self.data[x + 1][y].is_42_cell
        ):
            directions.append(((x, y), x + 1, y))
        if (
                cell.wall & SOUTH == 0
                and not self._data[x][y + 1].is_visited
                and not self._data[x][y + 1].is_42_cell
        ):
            directions.append(((x, y), x, y + 1))
        if (
                cell.wall & WEST == 0
                and not self._data[x - 1][y].is_visited
                and not self._data[x - 1][y].is_42_cell
        ):
            directions.append(((x, y), x - 1, y))
        return directions

    def solve(self, animate: bool = True) -> None:
        if self.found_path:
            return None
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
            if animate:
                sleep(DISPLAY_INTERVAL)
            directions.extend(self.find_directions(self._data[new_x][new_y]))

        x, y = self.exit
        while True:
            x_parent, y_parent = self._data[x][y].parent
            if (x_parent, y_parent) == self.entry:
                break
            self.path.append((x_parent, y_parent))
            self._data[x_parent][y_parent].color = rgb(106, 214, 205)
            if animate:
                sleep(DISPLAY_INTERVAL)
            x, y = self._data[x][y].parent
        self.path.reverse()
        for p in all_path:
            x, y = p
            self._data[x][y].color = CELL_COLOR
        for p in self.path:
            x, y = p
            self._data[x][y].color = rgb(106, 214, 205)
        if animate:
            sleep(DISPLAY_INTERVAL)
        self.found_path = True

    def start_solve(self, target: Any, args: Any) -> Thread | None:
        if self.solver_threading is not None \
                and self.solver_threading.is_alive():
            print("solve in progress...")
            return None
        self.solver_threading = Thread(target=target, args=args)
        self.solver_threading.daemon = True
        self.solver_threading.start()
        return self.solver_threading
