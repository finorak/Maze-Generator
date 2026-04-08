from typing import Any
from src.cell import Cell


def put_maze_into_file(file_name: str,
                       data: list[list[Cell]],
                       path: list[tuple[int, int]],
                       entry_pos: tuple[int, int],
                       end_pos: tuple[int, int]) -> None:
    def writing_path(
            output_file: Any,
            path: list[tuple[int, int]]) -> None:
        for x, y in path:
            cell = data[x][y]
            print(cell.parent)
            """
            if cell.wall & NORTH == 0:
                output_file.write("N")
            elif cell.wall & WEST == 0:
                output_file.write("W")
            elif cell.wall & EAST == 0:
                output_file.write("E")
            elif cell.wall & SOUTH == 0:
                    output_file.write("S")"""
        output_file.write("\n")

    with open(file_name, mode="w", encoding="utf-8") as output_file:
        for row in data:
            for cell in row:
                output_file.write(f"{cell.wall:X}")
            output_file.write("\n")
        output_file.write("\n")
        x, y = entry_pos
        end_x, end_y = end_pos
        output_file.write(f"{x}, {y}\n")
        output_file.write(f"{end_x}, {end_y}\n")
        writing_path(output_file, path)
