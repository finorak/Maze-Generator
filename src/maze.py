from threading import Thread
import random
from time import sleep
from typing import Any
from src.setting import (
    BLOCK_42_COLOR,
    CELL_STARTING_COLOR,
    DISPLAY_INTERVAL,
)
from .cell import Cell


class Maze:
    def __init__(self, entry_pos: tuple[int, int],
                 end_pos: tuple[int, int],
                 cols: int, rows: int,
                 perfect: bool = True, animate: bool = True) -> None:
        self.entry_pos = entry_pos
        self.end_pos = end_pos
        self.perfect = perfect
        self.data: list[list[Cell]] = []
        self.animate = animate
        self.block: list[tuple[int, int]] = []
        self.is_generate = False
        self.rows = rows
        self.cols = cols
        self.generation_thread: Thread | Any = None
        self.wall_destroyer:None | tuple[int, int] = None

    def init_data(self, show: bool = False) -> None:
        if len(self.data) == 0:
            self.data = [
                [
                    Cell(
                        row=i,
                        col=j,
                    )
                    for j in range(self.cols)
                ]
                for i in range(self.rows)
            ]
            if show:
                print(len(self.data), len(self.data[0]))
        else:
            for row in self.data:
                for cell in row:
                    cell.wall = 0b1111
                    cell.is_visited = False
                    cell.is_42_cell = False
                    cell.wall_closed = True
                    cell.parent = None
        self.make_42_block()
        if (
                self.entry_pos in self.block
                or self.end_pos in self.block
        ):
            print("Entry or Exit inside 42 block "
                  "Generating without 42 block")
            self.make_42_block(False)
        self.entry_pos = list(self.entry_pos)
        entry_x, entry_y = self.entry_pos
        if entry_x < 0 or entry_x >= self.rows:
            entry_x = 0
        if entry_y < 0 or entry_y >= self.cols:
            entry_y = 0
        self.entry_pos = (entry_x, entry_y)
        self.end_pos = list(self.end_pos)
        end_x, end_y = self.end_pos
        if end_x < 0 or end_x >= self.rows:
            end_x = self.rows - 1
        if end_y < 0 or end_y >= self.cols:
            end_y = self.cols - 1
        self.end_pos = (end_x, end_y)
        self.is_generate = False
        self.generation_thread = None

    def change_color(self, color: int, condition: str= "all") -> None:
        for row in self.data:
            for cell in row:
                c: bool = True
                if condition == "all":
                    c = True
                elif condition == "solve":
                    c = not cell.is_visited
                elif condition == "generate":
                    c = not cell.wall_closed
                if not cell.is_42_cell and c:
                    cell.color = color

    def make_42_block(self, show_logo: bool = True) -> None:
        if show_logo:
            color = BLOCK_42_COLOR
        else:
            color = CELL_STARTING_COLOR

        def set_four(x: int, y: int) -> None:
            for i in range(3):
                self.data[x][y + i].is_42_cell = show_logo
                self.data[x][y + i].color = color
                self.data[x + 2][y + 2 + i].is_42_cell = show_logo
                self.data[x + 2][y + 2 + i].color = color
                self.block.append((x, y + i))
                self.block.append((x + 2, y + 2 + i))
            self.data[x + 1][y + 2].is_42_cell = show_logo
            self.block.append((x + 1, y + 2))
            self.data[x + 1][y + 2].color = color

        def set_two(x: int, y: int) -> None:
            for i in range(3):
                self.data[x + i][y].is_42_cell = show_logo
                self.data[x + i][y].color = color
                self.data[x + i][y + 2].is_42_cell = show_logo
                self.data[x + i][y + 2].color = color
                self.data[x + i][y + 4].is_42_cell = show_logo
                self.data[x + i][y + 4].color = color
                self.block.append((x + i, y))
                self.block.append((x + i, y + 2))
                self.block.append((x + i, y + 4))
            self.data[x + 2][y + 1].is_42_cell = show_logo
            self.data[x + 2][y + 1].color = color
            self.data[x][y + 3].is_42_cell = show_logo
            self.data[x][y + 3].color = color
            self.block.append((x + 2, y + 1))
            self.block.append((x, y + 3))

        set_four(self.rows // 2 - 3, self.cols // 2 - 2)
        set_two(self.rows // 2 + 1, self.cols // 2 - 2)

    def find_neighbor_closed(
        self, cell_coord: tuple[int, int]
    ) -> list[tuple[str, str, int, int]]:
        neighbors: list[tuple[str, str, int, int]] = []
        x, y = cell_coord
        if (
            x + 1 < self.rows
            and self.data[x + 1][y].wall_closed
            and not self.data[x + 1][y].is_42_cell
        ):
            neighbors.append(("e", "w", x + 1, y))
        if (
            x - 1 >= 0
            and self.data[x - 1][y].wall_closed
            and not self.data[x - 1][y].is_42_cell
        ):
            neighbors.append(("w", "e", x - 1, y))
        if (
            y + 1 < self.cols
            and (self.data[x][y + 1].wall_closed
                 or not self.data[x][y + 1].is_visited)
            and not self.data[x][y + 1].is_42_cell
        ):
            neighbors.append(("s", "n", x, y + 1))
        if (
            y - 1 >= 0
            and self.data[x][y - 1].wall_closed
            and not self.data[x][y - 1].is_42_cell
        ):
            neighbors.append(("n", "s", x, y - 1))
        return neighbors

    def start_generate(self, start_pos: tuple[int, int] = (0, 0)) -> None:
        if self.generation_thread is not None \
                and self.generation_thread.is_alive():
            print("generate in progress...")
            return
        self.generation_thread = Thread(
                target=self.generete,
                args=(start_pos,))
        self.generation_thread.daemon = True
        self.generation_thread.start()

    def generete(self, start_pos: tuple[int, int] = (0, 0)) -> None:
        perfect = not self.perfect
        self.generate_maze(start_pos)
        self.break_wall(int(perfect) * 25 / 100)
        """
        COLORING ENTRY AND END POINT
        """
        self.is_generate = True
        self.wall_destroyer = None

    def generate_maze(self, start_pos: tuple[int, int]) -> None:
        self.wall_destroyer = start_pos
        start_x, start_y = start_pos
        cell = self.data[start_x][start_y]
        cell.wall_closed = False
        neightboors = self.find_neighbor_closed((start_x, start_y))
        random.shuffle(neightboors)
        for neightboor in neightboors:
            wall1, wall2, new_x, new_y = neightboor
            self.wall_destroyer = (new_x, new_y)
            self.data[new_x][new_y].updated = False
            if not self.data[new_x][new_y].wall_closed:
                continue
            cell.remove_wall(wall1)
            self.data[new_x][new_y].remove_wall(wall2)
            sleep(DISPLAY_INTERVAL)
            self.generate_maze((new_x, new_y))
        sleep(DISPLAY_INTERVAL)

    def break_wall(self, probability: float = 0.25) -> None:
        if probability == 0:
            return None
        walls = [("e", "w"), ("w", "e"), ("n", "s"), ("s", "n")]
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                x, y = i, j
                if random.random() < probability:
                    wall1, wall2 = random.choice(walls)
                    if (
                            wall1 == "s"
                            and y < self.cols - 1
                            and not self.data[x][y + 1].is_42_cell
                    ):
                        self.data[x][y].remove_wall(wall1)
                        self.data[x][y].wall_closed = False
                        self.data[x][y + 1].remove_wall(wall2)
                        self.data[x][y + 1].wall_closed = False
                    if (
                            wall1 == "n"
                            and y - 1 > 0
                            and not self.data[x][y - 1].is_42_cell
                    ):
                        self.data[x][y].remove_wall(wall1)
                        self.data[x][y].wall_closed = False
                        self.data[x][y - 1].remove_wall(wall2)
                        self.data[x][y - 1].wall_closed = False
                    if (
                            wall1 == "w"
                            and x - 1 > 0
                            and not self.data[x - 1][y].is_42_cell
                    ):
                        self.data[x][y].remove_wall(wall1)
                        self.data[x][y].wall_closed = False
                        self.data[x - 1][y].remove_wall(wall2)
                        self.data[x - 1][y].wall_closed = False
                    if (
                            wall1 == "e"
                            and x < self.rows - 1
                            and not self.data[x + 1][y].is_42_cell
                    ):
                        self.data[x][y].remove_wall(wall1)
                        self.data[x][y].wall_closed = False
                        self.data[x + 1][y].remove_wall(wall2)
                        self.data[x + 1][y].wall_closed = False
                    sleep(DISPLAY_INTERVAL)
