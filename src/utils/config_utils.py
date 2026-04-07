from time import sleep
from typing import Any


def custom_print(text: Any,
                 delimiter: str = "\n",
                 timer: float = 0.08) -> None:
    text_len = len(text)
    for i in range(text_len):
        print(text[i], flush=True, end="" if i < text_len - 1 else delimiter)
        sleep(timer)


def get_config(config: dict[str, Any],
               start: bool = True) -> bool:
    if start:
        custom_print("GETTING CONFIG FILE...")
    error = False
    sleep(0.01)
    for key, value in config.items():
        checker = "[0K]"
        custom_print(key, " : ")
        sleep(0.01)
        if (isinstance(value, int) and (key == "width"
                                        or key == "height")):
            if value >= 30 or value <= 0:
                checker = "[ERROR]"
                error = True
        if isinstance(value, str) and key == "perfect":
            if value not in ("true", "false"):
                checker = "[ERROR]"
                error = True
        if (
                isinstance(value, tuple)
                and (key == "entry" or key == "exit")):
            if (value[0] < 0 > value[1]):
                checker = "[ERROR]"
                error = True
        custom_print(f"{value} {checker}")
    return error
