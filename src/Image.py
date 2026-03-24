from typing import Any


class Image:
    def __init__(self) -> None:
        self.img: Any = None
        self.width = 0
        self.height = 0
        self.data: Any = None
        self.bpp = 0
        self.sl = 0
        self.ioformat = 0
