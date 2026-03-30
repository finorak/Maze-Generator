"""
The main program for our maze generator
"""

try:
    from src.app import App
except Exception as e:
    print(e)
try:
    from src.utils import get_configuration
except Exception as e:
    print(e)

if __name__ == "__main__":
    message: str | None = None
    # file_name = sys.argv[1]
    try:
        config = get_configuration("config.txt")
        print((config.get("width"), config.get("height")))
        app = App(config)
        app.run()
    except Exception as e:
        print(e)
