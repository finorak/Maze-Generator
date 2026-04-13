from typing import Any
from src.cell import Cell


def put_maze_into_file(file_name: str,
                       data: list[list[Cell]],
                       path: list[tuple[int, int]],
                       entry_pos: tuple[int, int],
                       end_pos: tuple[int, int]) -> None:
    path.reverse()
    def writing_path(
            output_file: Any,
            path: list[tuple[int, int]]) -> None:
        for x, y in path:
            cell = data[x][y]
            if cell.parent[1] == y + 1:
                output_file.write("N")
            elif cell.parent[0] == x + 1:
                output_file.write("W")
            elif cell.parent[0] == x - 1:
                output_file.write("E")
            elif cell.parent[1] == y - 1:
                output_file.write("S")
        output_file.write("\n")

    with open(file_name, mode="w", encoding="utf-8") as output_file:
        for i in range(len(data[0])):
            for j in range(len(data)):
                output_file.write(f"{data[j][i].wall:X}")
            output_file.write("\n")
        output_file.write("\n")
        x, y = entry_pos
        end_x, end_y = end_pos
        output_file.write(f"{x}, {y}\n")
        output_file.write(f"{end_x}, {end_y}\n")
        writing_path(output_file, path)
