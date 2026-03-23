from typing import Any, Union

from src.setting import HEIGHT, WIDTH, TITLE
from . import Cell
from . import get_configuration


class Maze:
    def __init__(self, mlx: Any):
        self.cells: list[list[Cell]] | Any = []
        self.mlx = mlx
        self.cell_width = 40
        self.cell_height = 40
        self.win_width = 500
        self.win_height = 500
        self.perfect = False

    def _init(self) -> bool:
        try:
            self.running = True
            self.mlx_init = self.mlx()
            self.mlx_ptr = self.mlx.mlx_init()
            self.mlx_window = self.mlx.mlx_new_window(
                self.mlx_ptr, WIDTH, HEIGHT, TITLE
                )
            self.mlx.mlx_loop(self.mlx_ptr)
            self.cells = self.get_cells()
            self.draw_grid()
            return True
        except Exception as e:
            print(e)
            return False

    def get_config(self, file_name: str
                   ) -> dict[str, Union[tuple, bool, tuple[int]]] | Any:
        config = get_configuration(file_name)
        if not config:
            return
        self.rows = config['width']
        self.cols = config['height']
        try:
            self.perfect = config['perfect']
        except Exception:
            pass
        self.exit = config['exit']
        self.entry = config['entry']
        self.output_file = config['output_file']
        if not isinstance(self.rows, int) or not \
                isinstance(self.cols, int):
            return None
        self.win_width = self.rows * self.cell_width
        self.win_height = self.cols * self.win_height
        return config

    def generate(self) -> None:
        if not self._init():
            return

    def get_cells(self) -> list[Cell] | Any:
        cells = []
        if not isinstance(self.rows, int) or not \
                isinstance(self.cols, int):
            return None
        for row in range(self.rows):
            cells.append([])
            for col in range(self.cols):
                cell = Cell(row, col, 0b1111,
                            self.cell_width, self.cell_height)
                cells.append(cell)
        return cells

    def draw_grid(self) -> None:
        """
        Might delete later
        """
        width_gap = WIDTH // self.cell_width
        height_gap = HEIGHT // self.cell_height
        if not isinstance(self.rows, int) or not \
                isinstance(self.cols, int):
            return
        for i in range(self.rows):
            for j in range(self.cols):
                pass
