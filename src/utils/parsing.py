"""
Utils module
This module contains the basique utils function we need
might use class later on
"""
from typing import Mapping, Union, Any


def config_is_valid(config: dict[str, Union[str, int, tuple, bool]]
                    ) -> bool:
    """
    This function verify if the config is vaild or not
    """
    if config is None:
        return False
    if "width" not in config or "height" not in config or not \
            config.get('width') or not config.get('height'):
        return False
    if not isinstance(config["width"], int) or not \
            isinstance(config["height"], int):
        return False
    if "entry" not in config or "exit" not in config:
        return False
    if not config.get('entry') or not isinstance(config["entry"], tuple):
        print(config)
        return False
    if not isinstance(config["entry"][0], int) or not \
            isinstance(config["entry"][1], int):
        return False
    if not config.get('exit') or not isinstance(config["exit"], tuple):
        return False
    if not isinstance(config['exit'][0], int) or not \
            isinstance(config["exit"][1], int):
        return False
    return True


def parse_config(config: dict[str, Any]
                 ) -> dict[str, Union[bool, tuple, int]]:
    """
    Parsing the config we got from get_configuration
    """
    conf: Mapping = {}
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
                      ) -> dict[str, Union[bool, tuple[int, int]]]:
    """
    Getting the configuration file using dict
    """
    config: dict[str, Any] | None = {}
    try:
        with open(file_name, mode="r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("#"):
                    continue
                line = line.strip().split("=")
                if len(line) != 2:
                    continue
                key: str = line[0]
                value: Union[str, tuple[int, int], int, bool] = line[1]
                pos = value.strip().split(",")
                if len(pos) == 2:
                    x = int(pos[0].strip())
                    y = int(pos[1].strip())
                    value = (x, y)
                config.update({key.strip().lower(): value})
        config = parse_config(config)
        if not config_is_valid(config):
            raise Exception("Config file is not valid")
        return config
    except Exception:
        raise Exception("Config file not provided")
