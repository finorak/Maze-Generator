"""
The main program for our maze generator
"""

import sys
from src.app import App
from src.utils import get_configuration

if __name__ == "__main__":
    message: str | None = None
    # file_name = sys.argv[1]
    try:
        config = get_configuration("config.txt")
    except Exception as e:
        message = e
    print((config.get("width"), config.get("height")))
    app = App(config)
    app.run()
