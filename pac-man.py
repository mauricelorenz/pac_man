import sys
from src.parser import parse_config


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py <config_file>", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    try:
        parse_config(path)
    except OSError as e:
        print(f"Error while reading {path}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
