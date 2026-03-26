from ..cell import Cell
from typing import Any
from ..setting import NORTH, SOUTH, WEST, EAST
from collections import deque
from ..utils.color_genertor import rgb

class Solver:
    def __init__(
        self, data: list[list[Cell]], 
        ENTRY: tuple[int, int], EXIT: tuple[int, int],
        app: Any
    ) -> None:
        self.data = data
        self.entry = ENTRY
        self.exit = EXIT
        self.path: list[tuple[int, int]] = []
        self.app = app

    def dfs_solver(self, param) -> None:
        pass

    def find_directions(
        self, cell: Cell
    ) -> list[tuple[int, int]]:
        directions: list[tuple[tuple[int, int], int, int]] = []
        if cell.wall & NORTH == 0 and self.data[cell.row][cell.col - 1].is_visited == False:
            directions.append(((cell.row, cell.col), cell.row, cell.col - 1))
        if cell.wall & EAST == 0 and self.data[cell.row + 1][cell.col].is_visited == False:
            directions.append(((cell.row, cell.col), cell.row + 1, cell.col))
        if cell.wall & SOUTH == 0 and self.data[cell.row][cell.col + 1].is_visited == False:
            directions.append(((cell.row, cell.col), cell.row, cell.col + 1))
        if cell.wall & WEST == 0 and self.data[cell.row - 1][cell.col].is_visited == False:
            directions.append(((cell.row, cell.col), cell.row - 1, cell.col))
        return directions

    def solve(self) -> None:
        x, y = self.entry
        self.data[x][y].is_visited = True
        directions = deque(self.find_directions(self.data[x][y]))
        while directions:
            direction = directions.popleft()
            parent, new_x, new_y = direction
            self.data[new_x][new_y].is_visited = True
            self.data[new_x][new_y].parent = parent
            if (new_x, new_y) == self.exit:
                break
            self.data[new_x][new_y].color = rgb(214, 106, 151)
            self.app.draw_maze()
            directions.extend(self.find_directions(self.data[new_x][new_y]))
        
        x, y = self.exit
        while True:
            x_parent, y_parent = self.data[x][y].parent
            if (x_parent, y_parent) == self.entry:
                break
            self.path.append((x_parent, y_parent))
            self.data[x_parent][y_parent].color = rgb(106, 214, 205)
            self.app.draw_maze()
            x, y = self.data[x][y].parent
        
            
        
        
