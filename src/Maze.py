from typing import Any, Union
from src.setting import HEIGHT, WIDTH, TITLE
from . import Cell
from . import get_configuration


class Maze:
    def __init__(self, mlx: Any, file_name: str):
        self.cells: list[list[Cell]] | Any = []
        self._: Any = mlx
        self.file_name: str = file_name
        self.cell_width: int = 40
        self.cell_height: int = 40
        self.win_width: int = 500
        self.win_height: int = 500
        self.perfect: bool = False

    def _init(self) -> bool:
        try:
            self.mlx = self._()
            self.mlx_ptr = self.mlx.mlx_init()
            self.mlx_window = self.mlx.mlx_new_window(
                self.mlx_ptr, WIDTH, HEIGHT, TITLE
                )
            conf = self.get_config(self.file_name)
            if not conf:
                return False
            self.cells = self.get_cells()
            return True
        except Exception as e:
            print(e)
            return False

    def run(self):
        self.event_handler(self.mlx_ptr, self.mlx_window)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.draw_cell,
                               (self.mlx, self.mlx_ptr, self.mlx_window))
        self.mlx.mlx_loop(self.mlx_ptr)

    def get_config(self, file_name: str
                   ) -> dict[str, Union[tuple, bool, tuple[int, int]]] | Any:
        config = get_configuration(file_name)
        if not config:
            return None
        self.rows = config['width']
        self.cols = config['height']
        try:
            self.perfect = bool(config['perfect'])
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

    def generate(self) -> None:
        if not self._init():
            return None
        self.run()

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
                cells[row].append(cell)
        return cells

    def event_handler(self, mlx_ptr: Any, mlx_window: Any) -> None:
        self.mlx.mlx_hook(mlx_window, 33, 0, self.close, mlx_ptr)

    def close(self, mlx_ptr: Any) -> None:
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.mlx_window)
        self.mlx.mlx_release(mlx_ptr)

    def draw_cell(self, args: Any) -> None:
        mlx = args[0]
        mlx_ptr = args[1]
        mlx_win = args[2]
        for row in self.cells:
            for cell in row:
                cell.draw_cell(mlx, mlx_ptr, mlx_win)
