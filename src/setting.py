def rgb(r, g, b):
    return 255 << 24 | r << 16 | g << 8 | b

def rgba(r, g, b, a):
    o = int(a * 255)
    return o << 24 | r << 16 | g << 8 | b

WIDTH = 840
HEIGHT = 600
TITLE = "Mazing Generator and solver"
# Wall direction
NORTH = 0b0001
SOUTH = 0b0100
WEST = 0b1000
EAST = 0b0010
WALL_THICK = 2
CELL_COLOR = rgb(255,255,255)
WALL_COLOR = 0xFF000000
VISITED_COLOR = rgb(50,50,50)
BLOCK_42_COLOR = rgb(255,255,0)