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
                self.parent.set_pos()
                self.can_move = True
        if not self.can_move:
            return None
        x_temp, y_temp = self.x, self.y
        self.parent.maze.data[x_temp][y_temp].updated = False
        if key == 65361 and self.x - 1 >= 0:
            if self.is_valid(self.x, self.y, self.x - 1, self.y, WEST):
                self.x -= 1
        elif key == 65363 and self.x + 1 < self.parent.cols:
            if self.is_valid(self.x, self.y, self.x + 1, self.y, EAST):
                self.x += 1
        elif key == 65362 and self.y - 1 >= 0:
            if self.is_valid(self.x, self.y, self.x, self.y - 1, NORTH):
                self.y -= 1
        elif key == 65364 and self.y + 1 < self.parent.rows:
            if self.is_valid(self.x, self.y, self.x, self.y + 1, SOUTH):
                self.y += 1
        if (self.x, self.y) == self.parent.end_pos:
            self.parent.end_reached.play()
        self.parent.entry_pos = (self.x, self.y)

    def is_valid(self, x: int, y: int,
                 x_upper: int, y_upper: int,
                 wall: int) -> bool:
        if self.parent.maze.data[x][y].wall & wall:
            return False
        if self.parent.maze.data[x_upper][y_upper].is_42_cell:
            return False
        return True
