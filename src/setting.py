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
CELL_COLOR = rgb(255, 255, 255)
TRAVERSING_COLOR = rgb(98, 189, 166)
CELL_STARTING_COLOR = rgb(78, 82, 81)
CLEAR_COLOR = rgb(0, 0, 0)
VISITED_COLOR = rgb(50, 50, 50)
BLOCK_42_COLOR = rgb(0, 0, 0)
ENTRY_COLOR = rgb(214, 106, 151)
EXIT_COLOR = rgb(214, 106, 151)
WALL_COLOR = rgb(0, 0, 0)
WALL_COLOR_2 = rgb(255, 0, 0)
WALL_COLOR_3 = rgb(126, 200, 80)
WALL_COLOR_4 = rgb(86, 125, 70)
WALL_COLORS = [
        WALL_COLOR, WALL_COLOR_2, WALL_COLOR_3,
        WALL_COLOR_4
        ]
PATH_FOUND_COLOR = rgb(106, 214, 205)
STRING_HEIGHT_PADDDING = 100
STRING_WIDTH_PADDING = 100
DISPLAY_INTERVAL = 0.05
HELP_WIDTH = 520
HELP_HEIGHT = 660
CELL_SIZE = 40

BASE_CONFIG = {
        'width': 20,
        'height': 20,
        'entry': (0, 0),
        'exit': (19, 19),
        'output_file': 'maze.txt',
        'perfext': 'true'
        }

HELP_TEXT = [
        "Help / Controls",
        "",
        "Space : open the maze screen",
        "g     : generate the maze",
        "s     : solve with A* (shortest path)",
        "d     : solve with DFS",
        "c     : save the maze",
        "r     : reset the maze",
        "h     : open this help window",
        "u     : Change the wall color",
        "q/Esc : quit the application",
    ]
