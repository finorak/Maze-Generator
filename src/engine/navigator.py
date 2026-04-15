from typing import Any


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
        print(key)
        if key == 65361:
            self.x -= 1
        elif key == 65363:
            self.x += 1
        elif key == 65362:
            self.y -= 1
        elif key == 65364:
            self.y += 1
        self.parent.entry_pos = (self.x, self.y)
