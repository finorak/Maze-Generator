from typing import Any

from src.setting import EAST, NORTH, SOUTH, WEST


class PlayerNavigator:
    def __init__(self, parent: Any) -> None:
        self.parent = parent
        self.can_move = False
        self.x, self.y = self.parent.entry_pos
        self.keyboard = [65363, 65364, 65361, 65362]

    def move(self, key: Any, _param: Any) -> None:
        if key != ord("j") and key not in self.keyboard:
            return None
        if key == ord("j"):
            if not self.can_move:
                self.can_move = True
        if not self.can_move:
            return None
        x_temp, y_temp = self.x, self.y
        self.parent.maze.data[x_temp][y_temp].updated = False
        if key == 65361 and self.x - 1 >= 0:
            if self.parent.maze.data[self.x][self.y].wall & WEST:
                return None
            if self.parent.maze.data[self.x - 1][self.y].is_42_cell:
                return None
            self.x -= 1
        elif key == 65363 and self.x + 1 < self.parent.cols:
            if self.parent.maze.data[self.x][self.y].wall & EAST:
                return None
            if self.parent.maze.data[self.x + 1][self.y].is_42_cell:
                return None
            self.x += 1
        elif key == 65362 and self.y - 1 >= 0:
            if self.parent.maze.data[self.x][self.y].wall & NORTH:
                return None
            if self.parent.maze.data[self.x][self.y - 1].is_42_cell:
                return None
            self.y -= 1
        elif key == 65364 and self.y + 1 < self.parent.rows:
            if self.parent.maze.data[self.x][self.y].wall & SOUTH:
                return None
            if self.parent.maze.data[self.x][self.y + 1].is_42_cell:
                return None
            self.y += 1
        self.parent.entry_pos = (self.x, self.y)
