"""Maze solving algorithms.

Provides a simple DFS and BFS-like solver used to find a path from
entry to exit and animate the result.
"""

from collections import deque
from threading import Thread
from time import sleep
from typing import Any, Callable

from maze.cell import Cell
from src.setting import (
    DISPLAY_INTERVAL,
    EAST,
    NORTH,
    PATH_FOUND_COLOR,
    SOUTH,
    WEST,
)
from src.utils.color_genertor import rgb


class Solver:
    """Solve a maze grid and expose control for animated solving."""
    def __init__(
        self,
        data: list[list[Cell]],
        entry_pos: tuple[int, int],
        end_pos: tuple[int, int],
    ) -> None:
        self._data = data
        self.entry = entry_pos
        self.exit = end_pos
        self.path: list[tuple[int, int]] = []
        self.is_generate = False
        self.found_path = False
        self.remove_color = True
        self.solver_threading: Thread | Any = None
        self.show: tuple[bool, bool] = (True, True)

    @property
    def data(self) -> list[list[Cell]]:
        return self._data

    @data.setter
    def data(self, data: list[list[Cell]]) -> None:
        self.is_generate = False
        self._data = data

    def dfs_solver(
        self,
        get_color: Callable,
        func: Callable,
        curr_pos: tuple[int, int] = (0, 0),
    ) -> bool:
        """Recursive DFS solver used for animated search.

        Args:
            get_color: Callable that returns the current wall color.
            func: Function to call to update maze color state.
            curr_pos: Starting coordinate for this invocation.

        Returns:
            True if a path to `self.exit` was found.
        """
        if self.found_path:
            return False

        def solve_maze(curr_pos: tuple[int, int]) -> bool:
            if self.found_path:
                return True
            if curr_pos == self.exit:
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
                self._data[new_x][new_y].parent = parent
                if self.dfs_solver(
                    get_color, func=func, curr_pos=(new_x, new_y)
                ):
                    self.path.append((new_x, new_y))
                    # curr_cell.color = CELL_STARTING_COLOR
                    if self.remove_color:
                        func(get_color(), "all")
                        self.remove_color = False
                        self.found_path = True
                    sleep(DISPLAY_INTERVAL)
                    self.found_path = True
                    return True
                # self._data[new_x][new_y].color = CELL_COLOR
                sleep(DISPLAY_INTERVAL)
            sleep(DISPLAY_INTERVAL)
            return False

        return solve_maze(curr_pos)

    def find_directions(
        self, cell: Cell
    ) -> list[tuple[tuple[int, int], int, int]]:
        """Return available neighbor coordinates from a cell.

        Skips visited or logo cells.
        """
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

    def bfs_solver(
        self,
        get_color: Callable,
        func: Callable[[int, str], None],
        animate: bool = True,
    ) -> None:
        """Iteratively search for a path and mark the discovered route.

        Args:
            get_color: Callable that returns the current wall color.
            func: Function to call to update maze color state.
            animate: Whether to sleep between steps for animation.
        """
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
        func(get_color(), "all")
        self.found_path = True

    def start_solve(self, target: Any, args: Any) -> None:
        """Start the given solving function in a background thread.

        Args:
            target: Callable to run in background.
            args: Arguments tuple to pass to the target.
        """
        if (
            self.solver_threading is not None and
            self.solver_threading.is_alive()
        ):
            print("solve in progress...")
            return None
        self.solver_threading = Thread(target=target, args=args)
        self.solver_threading.daemon = True
        self.solver_threading.start()
