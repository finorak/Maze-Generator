"""
Utils module
This module contains the basique utils function we need
might use class later on
"""


def parse_config(config: dict[str, str | tuple]
                 ) -> dict[str, str | tuple | int]:
    """
    Parsing the config we got from get_configuration
    """
    conf = dict()
    for key, value in config.items():
        if isinstance(value, str) and value.isdigit():
            conf[key] = int(value)
        else:
            conf[key] = value
    return conf


def get_configuration(file_name: str) -> dict | None:
    """
    Getting the configuration file using dict
    """
    config = dict()
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
                pos = value.split(",")
                if len(pos) == 2:
                    value = tuple(map(int, pos))
                config.update({key: value})
        return parse_config(config)
    except Exception as e:
        print(e)
        return None
