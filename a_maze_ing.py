"""
The main program for our maze generator
"""

import sys
from src.App import App
from src.utils import get_configuration

if __name__ == "__main__":
    # file_name = sys.argv[1]
    config = get_configuration("config.txt")
    print((config.get("width"), config.get("height")))
    app = App(config)
    app.run()
