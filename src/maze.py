from typing import Any
from src.engine.solver import Solver
from src.setting import (
        BLOCK_42_COLOR, CELL_COLOR, CELL_STARTING_COLOR,
        ENTRY_COLOR, EXIT_COLOR, TRAVERSING_COLOR, VISITED_COLOR)
from .cell import Cell
from random import choice, shuffle
import random

class Maze:
    def __init__(self, parent: Any):
        self.data: list[list[Cell]] | Any = None
        self.height = 0
        self.width = 0
        self.parent = parent
        self.perfect = parent.config.get("perfect")
        self.entry_pos = self.parent.config.get('entry')
        self.end_pos = self.parent.config.get('exit')
        self.is_generate = False

    def init_data(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        self.data = [
            [
                Cell(row=i, col=j, cols=self.width, rows=self.height,
                     color=CELL_STARTING_COLOR
                     ) for j in range(self.height)
            ] for i in range(self.width)
        ]
        self.make_42_block()

    def make_42_block(self) -> None:
        color = BLOCK_42_COLOR

        def set_four(x: int, y: int) -> None:
            for i in range(3):
                self.data[x][y + i].is_42_cell = True
                self.data[x][y + i].color = color
                self.data[x + 2][y + 2 + i].is_42_cell = True
                self.data[x + 2][y + 2 + i].color = color
            self.data[x + 1][y + 2].is_42_cell = True
            self.data[x + 1][y + 2].color = color

        def set_two(x: int, y: int) -> None:
            for i in range(3):
                self.data[x + i][y].is_42_cell = True
                self.data[x + i][y].color = color
                self.data[x + i][y + 2].is_42_cell = True
                self.data[x + i][y + 2].color = color
                self.data[x + i][y + 4].is_42_cell = True
                self.data[x + i][y + 4].color = color
            self.data[x + 2][y + 1].is_42_cell = True
            self.data[x + 2][y + 1].color = color
            self.data[x][y + 3].is_42_cell = True
            self.data[x][y + 3].color = color

        set_four(self.width//2 - 3, self.height//2 - 2)
        set_two(self.width//2 + 1, self.height//2 - 2)

    def find_neighbor_closed(self,
                             cell_coord: tuple[int, int]
                             ) -> list[tuple[str, str, int, int]]:
        neighbors: list[tuple[str, str, int, int]] = []
        x, y = cell_coord
        if (x + 1 < self.width and self.data[x + 1][y].wall_closed
               and not self.data[x + 1][y].is_42_cell):
            neighbors.append(("e", "w", x + 1, y))
        if (x - 1 >= 0 and self.data[x - 1][y].wall_closed
                and not self.data[x - 1][y].is_42_cell):
            neighbors.append(("w", "e", x - 1, y))
        if (y + 1 < self.height and (self.data[x][y + 1].wall_closed 
                                   or not self.data[x][y + 1].is_visited) 
            and not self.data[x][y + 1].is_42_cell):
            neighbors.append(("s", "n", x, y + 1))
        if (y - 1 >= 0 and self.data[x][y - 1].wall_closed
                            and not self.data[x][y - 1].is_42_cell):
            neighbors.append(("n", "s", x, y - 1))
        return neighbors

    def generete(self, start_pos: tuple[int, int] = (0, 0)) -> None:

        # generating the maze
        self.generate_maze(start_pos, (int(self.perfect) * 30) / 100)
        """
        COLORING ENTRY AND END POINT
        """
        entry_x, entry_y = self.entry_pos
        entry_cell = self.data[entry_x][entry_y]
        entry_cell.color = ENTRY_COLOR
        self.parent.draw_cell(entry_cell)
        end_x, end_y = self.end_pos
        end_cell = self.data[end_x][end_y]
        end_cell.color = EXIT_COLOR
        self.parent.draw_cell(end_cell)
        self.is_generate = False

    def generate_maze(self, start_pos: tuple[int, int],
                        probability: float = 0) -> None:
        # self.parent.event_handler()
        start_x, start_y = start_pos
        cell = self.data[start_x][start_y]
        cell.wall_closed = False
        cell.color = VISITED_COLOR
        neightboors = self.find_neighbor_closed((start_x, start_y))
        shuffle(neightboors)
        for neightboor in neightboors:
            wall1, wall2, new_x, new_y = neightboor
            if not self.data[new_x][new_y].wall_closed:
                continue
            cell.remove_wall(wall1)
            self.data[new_x][new_y].color = TRAVERSING_COLOR
            self.data[new_x][new_y].remove_wall(wall2)
            self.parent.draw_maze()
            self.generate_maze((new_x, new_y))
            self.data[new_x][new_y].color = CELL_COLOR
            if random.random() < probability:
                curr_n = self.find_neighbor_closed((new_x, new_y))
                shuffle(curr_n)
                wall_1, wall_2, x, y = choice(curr_n)
                self.data[new_x][new_y].remove_wall(wall_1)
                c = self.data[x][y]
                c.remove_wall(wall_2)
        self.parent.draw_maze()

    def solve(self):
        solve = Solver(self.data, self.entry_pos, self.end_pos, self.parent)
        solve.dfs_solver(self.entry_pos)
