from typing import Any, Union
from src.setting import HEIGHT, WIDTH, TITLE
from . import Cell
from . import get_configuration


class Maze:
    def __init__(self, mlx: Any):
        self.cells: list[list[Cell]] | Any = []
        self._ = mlx
        self.cell_width = 40
        self.cell_height = 40
        self.win_width = 500
        self.win_height = 500
        self.perfect = False

    def _init(self) -> bool:
        try:
            self.running = True
            self.mlx = self._()
            self.mlx_ptr = self.mlx.mlx_init()
            self.mlx_window = self.mlx.mlx_new_window(
                self.mlx_ptr, WIDTH, HEIGHT, TITLE
                )
            self.event_handler(self.mlx_ptr, self.mlx_window)
            self.mlx.mlx_loop(self.mlx_ptr)
            return True
        except Exception as e:
            print(e)
            return False

    def get_config(self, file_name: str
                   ) -> dict[str, Union[tuple, bool, tuple[int]]] | Any:
        config = get_configuration(file_name)
        if not config:
            return None
        self.rows = config['width']
        self.cols = config['height']
        try:
            self.perfect = config['perfect']
        except Exception:
            pass
        if not config.get('exit') or not config.get('entry') or not \
                isinstance(config['exit'], tuple) or not \
                isinstance(config['entry'], tuple):
            return None
        self.exit = config['exit']
        self.entry = config['entry']
        self.output_file = config['output_file']
        if not isinstance(self.rows, int) or not \
                isinstance(self.cols, int):
            return None
        self.win_width = self.rows * self.cell_width
        self.win_height = self.cols * self.win_height
        return config

    def generate(self, file_name) -> None:
        config = self.get_config(file_name)
        if not self._init() or not config:
            return None

    def get_cells(self) -> list[Cell] | Any:
        cells: Any = []
        if not isinstance(self.rows, int) or not \
                isinstance(self.cols, int):
            return None
        for row in range(self.rows):
            cells.append([])
            for col in range(self.cols):
                cell = Cell(row, col,
                            self.cell_width, self.cell_height,
                            self.win_width, self.win_height
                            )
                cells.append(cell)
        return cells

    def draw_grid(self) -> None:
        """
        Might delete later
        """
        width_gap = WIDTH // self.cell_width
        height_gap = HEIGHT // self.cell_height
        _ = width_gap, height_gap
        if not isinstance(self.rows, int) or not \
                isinstance(self.cols, int):
            return
        for i in range(self.rows):
            for j in range(self.cols):
                pass

    def event_handler(self, mlx_ptr: Any, mlx_window: Any) -> None:
        self.mlx.mlx_hook(mlx_window, 33, 0, self.close, mlx_ptr)

    def close(self, mlx_ptr: Any) -> None:
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.mlx_window)
        self.mlx.mlx_release(mlx_ptr)
