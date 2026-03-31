from threading import Thread
import random
from time import sleep
from typing import Any
from src.setting import (
    BLOCK_42_COLOR,
    CELL_COLOR,
    CELL_STARTING_COLOR,
    ENTRY_COLOR,
    EXIT_COLOR,
    TRAVERSING_COLOR,
    VISITED_COLOR,
    DISPLAY_INTERVAL,
)
from .cell import Cell


class Maze:
    def __init__(self, parent: Any):
        self.data: list[list[Cell]] | Any = None
        self.parent = parent
        self.perfect = parent.config.get("perfect")
        self.entry_pos = self.parent.config.get("entry")
        self.end_pos = self.parent.config.get("exit")
        self.is_generate = False
        self.generation_thread: Any = None

    def init_data(self, cols: int, rows: int) -> None:
        self.cols = cols
        self.rows = rows
        self.data = [
            [
                Cell(
                    row=i,
                    col=j,
                    cols=self.rows,
                    rows=self.cols,
                    color=CELL_STARTING_COLOR,
                )
                for j in range(self.cols)
            ]
            for i in range(self.rows)
        ]
        self.make_42_block()
        self.is_generate = False

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
        entry_x, entry_y = self.entry_pos
        entry_cell = self.data[entry_x][entry_y]
        entry_cell.color = ENTRY_COLOR
        end_x, end_y = self.end_pos
        end_cell = self.data[end_x][end_y]
        end_cell.color = EXIT_COLOR
        self.is_generate = True

    def generate_maze(self, start_pos: tuple[int, int]) -> None:
        start_x, start_y = start_pos
        cell = self.data[start_x][start_y]
        cell.wall_closed = False
        cell.color = VISITED_COLOR
        neightboors = self.find_neighbor_closed((start_x, start_y))
        random.shuffle(neightboors)
        for neightboor in neightboors:
            wall1, wall2, new_x, new_y = neightboor
            if not self.data[new_x][new_y].wall_closed:
                continue
            cell.remove_wall(wall1)
            self.data[new_x][new_y].color = TRAVERSING_COLOR
            self.data[new_x][new_y].remove_wall(wall2)
            sleep(DISPLAY_INTERVAL)
            self.generate_maze((new_x, new_y))
            self.data[new_x][new_y].color = CELL_COLOR
        sleep(DISPLAY_INTERVAL)

    def break_wall(self, probability: float = 0.25) -> None:
        if probability == 0:
            return None
        walls = [("e", "w"), ("w", "e"), ("n", "s"), ("s", "n")]
        for i in range(len(self.data)):
            row: list[Cell] = self.data[i][:]
            random.shuffle(row)
            for j in range(len(row)):
                x, y = i, j
                if random.random() < probability:
                    wall1, wall2 = random.choice(walls)
                    if wall1 == "s" and y + 1 < self.cols:
                        self.data[x][y].remove_wall(wall1)
                        self.data[x][y].wall_closed = False
                        self.data[x][y + 1].remove_wall(wall2)
                        self.data[x][y + 1].wall_closed = False
                    if wall1 == "n" and y - 1 > 0:
                        self.data[x][y].remove_wall(wall1)
                        self.data[x][y].wall_closed = False
                        self.data[x][y - 1].remove_wall(wall2)
                        self.data[x][y - 1].wall_closed = False
                    if wall1 == "w" and x - 1 > 0:
                        self.data[x][y].remove_wall(wall1)
                        self.data[x][y].wall_closed = False
                        self.data[x - 1][y].remove_wall(wall2)
                        self.data[x - 1][y].wall_closed = False
                    if wall1 == "e" and x < self.rows - 1:
                        self.data[x][y].remove_wall(wall1)
                        self.data[x][y].wall_closed = False
                        self.data[x + 1][y].remove_wall(wall2)
                        self.data[x + 1][y].wall_closed = False
                    sleep(DISPLAY_INTERVAL)
