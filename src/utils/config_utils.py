"""Helpers for printing and validating configuration dictionaries.

This module provides a small helper to pretty-print text and a
validation routine for configuration dictionaries used by the
application.
"""

from typing import Any


def custom_print(text: Any,
                 delimiter: str = "\n",
                 timer: float = 0.08) -> None:
    """Print text in a controlled manner (placeholder for animated output).

    Args:
        text: Text to print (iterable like string supported).
        delimiter: Trailing delimiter to use when finished.
        timer: Unused delay placeholder.
    """
    text_len = len(text)
    for i in range(text_len):
        print(text[i], flush=False, end="" if i < text_len - 1 else delimiter)
        # sleep(timer)


def get_config(config: dict[str, Any],
               start: bool = True) -> bool:
    """Validate and print configuration entries, returning error flag.

    Args:
        config: Configuration dictionary to validate.
        start: If True, prints a header message.

    Returns:
        True when any validation error is found, otherwise False.
    """
    if start:
        custom_print("GETTING CONFIG FILE...")
    error = False
    width = config.get('width')
    height = config.get('height')
    if width is None or height is None:
        return False
    for key, value in config.items():
        checker = "[0K]"
        custom_print(key, " : ")
        if (isinstance(value, int) and key in ("width", "height")):
            # if width <= 15 and height <= 15:
            #     checker = "[ERROR]"
            #     error = True
            if value <= 0:
                checker = "[ERROR]"
                error = True
        if isinstance(value, str) and key == "perfect":
            if value not in ("true", "false"):
                checker = "[ERROR]"
                error = True
        if isinstance(value, tuple) and (key in ("entry", "exit")):
            if config.get('entry') == config.get("exit"):
                checker = "[ERROR]"
                error = True
            if (value[0] < 0 > value[1]) or (
                    value[0] >= width or value[1] >= height):
                checker = "[ERROR]"
                error = True
        custom_print(f"{value} {checker}")
    return error
