"""
Utils module
This module contains the basique utils function we need
might use class later on
"""


from typing import Union


def config_is_valid(config: dict[str, str | int | tuple | bool] | None
                    ) -> bool:
    """
    This function verify if the config is vaild or not
    """
    if config is None:
        return False
    if "width" not in config or "height" not in config:
        return False
    if not isinstance(config["width"], int) or not \
            isinstance(config["height"], int):
        return False
    if "entry" not in config or "exit" not in config:
        return False
    if not isinstance(config["entry"], tuple):
        return False
    if not isinstance(config["entry"][0], int) or not \
            isinstance(config["entry"][1], int):
        return False
    if not isinstance(config["exit"], tuple):
        return False
    if not isinstance(config["exit"][0], int) or not \
            isinstance(config["exit"][1], int):
        return False
    return True


def parse_config(config: dict[str, str | tuple]
                 ) -> dict[str, Union[bool, tuple, int]]:
    """
    Parsing the config we got from get_configuration
    """
    conf = dict()
    for key, value in config.items():
        if isinstance(value, str) and value.isdigit():
            conf[key] = int(value)
        elif isinstance(value, str) and value.lower() == "true":
            conf[key] = True
        elif isinstance(value, str) and value.lower() == "false":
            conf[key] = False
        else:
            conf[key] = value
    return conf


def get_configuration(file_name: str
                      ) -> dict[str, Union[bool, tuple[int]]] | None:
    """
    Getting the configuration file using dict
    """
    config: dict | None = dict()
    try:
        with open(file_name, mode="r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("#"):
                    continue
                line = line.strip().split("=")
                if len(line) != 2:
                    return None
                key, value = line
                pos = value.strip().split(",")
                if len(pos) == 2:
                    value = int(pos[0].strip()), int(pos[1].strip())
                config.update({key.lower(): value})
        config = parse_config(config)
        if not config_is_valid(config):
            return None
        return config
    except Exception as e:
        print(e)
        return None
