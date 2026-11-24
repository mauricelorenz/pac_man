import sys

from src.parser import parse_config
from src.game_core.game import CoreGameEngine


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py <config_file>", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    try:
        config_file = parse_config(path)
    except OSError as e:
        print(f"Cannot open '{path}': {e.strerror or e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Invalid content in file '{path}': {e}", file=sys.stderr)
        sys.exit(1)

    engine = CoreGameEngine(config=config_file)
    engine.run_loop()


if __name__ == "__main__":
    main()
