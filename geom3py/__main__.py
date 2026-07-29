import argparse
from . import __version__


def main():
    parser = argparse.ArgumentParser(
        prog="geom3py",
        description="Library for 3D analytical geometry."
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    parser.parse_args()


if __name__ == "__main__":
    main()