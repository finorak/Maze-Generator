"""
The main program for our maze generator
"""

try:
    from src.app import App
    from src.utils import get_configuration
    from src.setting import BASE_CONFIG
except Exception as e:
    print(e)


if __name__ == "__main__":
    message: str | None = None
    # file_name = sys.argv[1]
    try:
        config = get_configuration("config.txt")
        app = App(config)
        app.run()
    except Exception as e:
        print(e)
