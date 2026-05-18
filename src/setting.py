"""Application settings and constants.

This module exposes configuration constants used across the
maze generator and helper functions for resolving asset paths.
"""

import os

from src.utils import rgb

WALL_COLORS = [
    rgb(0, 255, 255),
    rgb(38, 41, 196),
    rgb(200, 50, 255),
    rgb(255, 120, 0),
    rgb(255, 200, 50),
]

WIDTH = 800
HEIGHT = 600
TITLE = "Mazing Generator and solver"
# Wall direction
NORTH = 0b0001
SOUTH = 0b0100
WEST = 0b1000
EAST = 0b0010
PATH_FOUND_COLOR = rgb(106, 214, 205)
STRING_HEIGHT_PADDDING = 100
STRING_WIDTH_PADDING = 100
DISPLAY_INTERVAL = 0.02
HELP_WIDTH = 800
HELP_HEIGHT = 600
CELL_SIZE = 40

BASE_CONFIG = {
    "width": 16,
    "height": 16,
    "entry": (0, 0),
    "exit": (15, 15),
    "output_file": "maze.txt",
    "perfext": "true",
}

IMAGES = {
    "home": "assets/home.png",
    "help": "assets/help.png",
    "entry": "assets/path/entry.png",
    "exit": "assets/path/exit.png",
    "path": "assets/path/path.png",
    "0000": "assets/cell/0000.png",
    "0001": "assets/cell/0001.png",
    "0010": "assets/cell/0010.png",
    "0011": "assets/cell/0011.png",
    "0100": "assets/cell/0100.png",
    "0101": "assets/cell/0101.png",
    "0110": "assets/cell/0110.png",
    "0111": "assets/cell/0111.png",
    "1000": "assets/cell/1000.png",
    "1001": "assets/cell/1001.png",
    "1010": "assets/cell/1010.png",
    "1011": "assets/cell/1011.png",
    "1100": "assets/cell/1100.png",
    "1101": "assets/cell/1101.png",
    "1110": "assets/cell/1110.png",
    "1111": "assets/cell/1111.png",
}


def get_path(BASE_DIR: str, file_name: str) -> str:
    """Return normalized path to an asset in the `assets/vfx` folder.

    Args:
        BASE_DIR: Base directory of the calling module.
        file_name: Filename inside the `vfx` assets folder.

    Returns:
        Normalized filesystem path to the asset.
    """
    return os.path.normpath(
            os.path.join(BASE_DIR, "..", "assets", "vfx", file_name)
            )
