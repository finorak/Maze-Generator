"""
Utils module
This module contains the basique utils function we need
might use class later on
"""
from typing import Union, Any
from src.utils.config_utils import get_config, custom_print


def config_is_valid(config: dict[str, Any]
                    ) -> bool:
    """
    This function verify if the config is vaild or not
    """
    if config is None:
        return False
    if get_config(config):
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
        return False
    if not isinstance(config["entry"][0], int) or not \
            isinstance(config["entry"][1], int):
        return False
    if not config.get('exit') or not isinstance(config["exit"], tuple):
        return False
    if not isinstance(config['exit'][0], int) or not \
            isinstance(config["exit"][1], int):
        return False
    if config['entry'] == config['exit']:
        return False
    if config['height'] <= 0 or config['height'] <= 0:
        return False
    if config['entry'][0] < 0 or config['entry'][1] < 0:
        return False
    if config['exit'][0] < 0 or config['exit'][1] < 0:
        return False
    return True


def parse_config(config: dict[str, Any]
                 ) -> dict[str, Any]:
    """
    Parsing the config we got from get_configuration
    """
    conf: dict[str, Any] = {}
    for key, value in config.items():
        if isinstance(value, str) and value.isdigit():
            conf[key] = int(value)
        elif isinstance(value, str) and value.lower() == "true":
            conf[key] = True
        elif isinstance(value, str) and value.lower() == "false":
            conf[key] = False
        else:
            try:
                conf[key] = int(value)
            except Exception:
                conf[key] = value
    return conf


def get_configuration(
        file_name: str
        ) -> dict[str, Any] | None:
    """
    Getting the configuration file using dict
    """
    from src.setting import BASE_CONFIG
    config: dict[str, Any] = {}
    try:
        with open(file_name, mode="r", encoding="utf-8") as file:
            lines = file.readlines()
            if not lines:
                print("No config given")
                return {}
            for line in lines:
                if line.startswith("#"):
                    continue
                new_line: list[str] = line.strip().split("=")
                if len(new_line) != 2:
                    continue
                key: str = new_line[0].strip(" \t\r")
                value: Union[str, Any] = new_line[1].strip(" \t\r")
                pos = value.strip().split(",")
                if len(pos) == 2:
                    x = int(pos[0].strip())
                    y = int(pos[1].strip())
                    value = (x, y)
                config.update({key.strip().lower(): value})
        config = parse_config(config)
        if not config_is_valid(config):
            print("\nCONFIG ERROR !!!")
            custom_print("SWITCHING TO BASE_CONFIG")
            get_config(BASE_CONFIG)
            return BASE_CONFIG
        return config
    except Exception as e:
        print(e)
        return None
