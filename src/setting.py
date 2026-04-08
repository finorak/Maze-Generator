from .utils import rgb


WIDTH = 840
HEIGHT = 600
TITLE = "Mazing Generator and solver"
# Wall direction
NORTH = 0b0001
SOUTH = 0b0100
WEST = 0b1000
EAST = 0b0010
WALL_THICK = 2
CELL_COLOR = rgb(223, 221, 142)
TRAVERSING_COLOR = rgb(98, 189, 166)
CELL_STARTING_COLOR = rgb(223, 221, 142)
WALL_COLOR = rgb(0, 0, 0)
CLEAR_COLOR = rgb(0, 0, 0)
VISITED_COLOR = rgb(223, 221, 142)
BLOCK_42_COLOR = rgb(200, 250, 0)
ENTRY_COLOR = rgb(214, 106, 151)
EXIT_COLOR = rgb(106, 214, 205)
PATH_FOUND_COLOR = rgb(106, 214, 205)
WALL_COLOR = rgb(0, 0, 0)
WALL_COLOR_2 = rgb(255, 0, 0)
WALL_COLORS = [WALL_COLOR, WALL_COLOR_2]
STRING_HEIGHT_PADDDING = 100
STRING_WIDTH_PADDING = 100
DISPLAY_INTERVAL = 0.1
HELP_WIDTH = 520
HELP_HEIGHT = 660
CELL_SIZE = 40
BASE_CONFIG = {
        'width': 9,
        'height': 7,
        'entry': (2, 0),
        'exit': (3, 0),
        'output_file': 'maze.txt',
        'perfext': 'true'
        }
HELP_TEXT = [
        "Help / Controls",
        "",
        "Space : open the maze screen",
        "g     : generate the maze",
        "s     : solve with A*",
        "d     : solve with DFS",
        "c     : save the maze",
        "r     : reset the maze",
        "h     : open this help window",
        "q/Esc : quit the application",
    ]

IMAGES = {
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




















