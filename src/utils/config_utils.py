from time import sleep
from typing import Any

from src import setting


def custom_print(text: Any,
                 delimiter: str = "\n",
                 timer: float = 0.08) -> None:
    text_len = len(text)
    for i in range(text_len):
        print(text[i], flush=False, end="" if i < text_len - 1 else delimiter)
        # sleep(timer)


def get_config(config: dict[str, Any],
               start: bool = True) -> bool:
    if start:
        custom_print("GETTING CONFIG FILE...")
    error = False
    width = config.get('width')
    height = config.get('height')
    for key, value in config.items():
        checker = "[0K]"
        custom_print(key, " : ")
        if (isinstance(value, int) and key in ("width", "height")):
            if value >= 30 or value <= 0:
                checker = "[ERROR]"
                error = True
        if isinstance(value, str) and key == "perfect":
            if value not in ("true", "false"):
                checker = "[ERROR]"
                error = True
        if isinstance(value, tuple) and (key in ("entry", "exit")):
            if (value[0] < 0 > value[1]) or (
                    value[0] >= width or value[1] >= height):
                checker = "[ERROR]"
                error = True
        custom_print(f"{value} {checker}")
    return error
