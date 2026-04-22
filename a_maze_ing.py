"""
The main program for our maze generator
"""
import sys

try:
    from src.app import App
    from src.utils.parsing import get_configuration
except Exception as e:
    print(e)
    sys.exit(1)


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print("No argument given")
            sys.exit(1)
        config = get_configuration(
                sys.argv[1]
                )
        if not config or config is None:
            sys.exit(1)
        app = App(config)
        app.run()
    except Exception as e:
        print(e)
