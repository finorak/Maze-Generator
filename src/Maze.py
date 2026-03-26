from os import PRIO_PGRP
from typing import Any
from src.setting import BLOCK_42_COLOR, CELL_COLOR, ENTRY_COLOR, EXIT_COLOR, VISITED_COLOR
from src.utils.color_genertor import rgb
from .Cell import Cell
from . import DIRECTIONS
from random import choice, shuffle
import random
import time
from multiprocessing import Process


class Maze:
    def __init__(self, parent: Any):
        self.data: list[list[Cell]] | Any = None
        self.rows = 0
        self.cols = 0
        self.parent = parent
        self.perfect = parent.config.get("perferct")
        self.entry_pos = self.parent.config.get('entry')
        self.end_pos = self.parent.config.get('exit')

    def init_data(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.data = [
            [
                Cell(i, j, self.cols, self.rows) for j in range(self.rows)
            ] for i in range(self.cols)
        ]
        self.make_42_block()

    def make_42_block(self):
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

        set_four(self.cols//2 - 3, self.rows//2 - 2)
        set_two(self.cols//2 + 1, self.rows//2 - 2)

    def find_neighbor_closed(self,
                             cell_coord: tuple[int, int]
                             ) -> list[tuple[str, str, int, int]]:
        neighbors: list[tuple[str, str, int, int]] = []
        x, y = cell_coord
        if (x + 1 < self.cols and (self.data[x + 1][y].wall_closed \
                and not self.data[x + 1][y].is_42_cell)):
            neighbors.append(("e", "w", x + 1, y))
        if (x - 1 >= 0 and (self.data[x - 1][y].wall_closed and not \
                self.data[x - 1][y].is_42_cell)):
            neighbors.append(("w", "e", x - 1, y))
        if (y + 1 < self.rows and (self.data[x][y + 1].wall_closed \
                and not self.data[x][y + 1].is_42_cell)):
            neighbors.append(("s", "n", x, y + 1))
        if (y - 1 >= 0 and (self.data[x][y - 1].wall_closed and not \
                self.data[x][y - 1].is_42_cell)):
            neighbors.append(("n", "s", x, y - 1))
        return neighbors

    def generete(self):
        if self.perfect:
            self.generate_perfect_maze()
        else:
            self.generate_non_perfect_maze(self.entry_pos)
        entry_x, entry_y = self.entry_pos
        entry_cell = self.data[entry_x][entry_y]
        entry_cell.color = ENTRY_COLOR
        self.parent.draw_cell(entry_cell)
        end_x, end_y = self.end_pos
        end_cell = self.data[end_x][end_y]
        end_cell.color = EXIT_COLOR
        self.parent.draw_cell(end_cell)

    def generate_perfect_maze(self, x = 0, y = 0):
        self.data[x][y].wall_closed = False
        neighbors = self.find_neighbor_closed((x, y))

        neighbor = random.choice(neighbors)
        wall1, wall2, new_x, new_y = neighbor
        self.data[x][y].remove_wall(wall1)
        self.parent.draw_cell(self.data[x][y])
        self.data[new_x][new_y].remove_wall(wall2)
        self.parent.draw_cell(self.data[new_x][new_y])
        self.generate_perfect_maze(new_x, new_y)
        

    def generate_non_perfect_maze(self,
                                  start_pos: tuple[int, int]
                                  ) -> None:
        def generate_maze(start_pos: tuple[int, int],
                          probability: float = 0) -> None:
            self.parent.event_handler()
            start_x, start_y = start_pos
            cell = self.data[start_x][start_y]
            cell.is_visited = True
            cell.color = VISITED_COLOR
            self.parent.draw_cell(cell)
            neightboors = self.find_neighbor_closed((start_x, start_y))
            shuffle(neightboors)
            for neightboor in neightboors:
                wall1, wall2, new_x, new_y = neightboor
                if not self.data[new_x][new_y].is_visited and not \
                    self.data[new_x][new_y].is_42_cell:
                    cell.remove_wall(wall1)
                    self.data[new_x][new_y].remove_wall(wall2)
                    if random.random() < probability:
                        print("removing")
                        wall_1, wall_2, x, y = choice(neightboors)
                        cell.remove_wall(wall_1)
                        c = self.data[x][y]
                        c.remove_wall(wall_2)
                    self.parent.draw_maze()
                    generate_maze((new_x, new_y))
                    self.data[new_x][new_y].color = CELL_COLOR
                    self.parent.draw_maze()
        generate_maze(start_pos, 0.2)
