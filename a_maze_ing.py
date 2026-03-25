"""
The main program for our maze generator
"""

from src.App import App

if __name__ == "__main__":
    config = {"width":0, "height":0}
    app = App(config)
    app.run()
