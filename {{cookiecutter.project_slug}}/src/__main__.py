"""The main entry point."""
import argparse
import cli

parser = argparse.ArgumentParser(
    prog="dispatch",
    description="Dispatch the functional flow.",
    epilog="Good luck.",
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="output detailed info to the console.",
)
parser.add_argument(
    "process",
    action="store",
    choices=["etl"],
    help="The name of the process.",
)
parser.add_argument(
    "-s",
    "--single",
    action="store_false",
    help="Default is False. If true, process the step alone.",
)
args = parser.parse_args()


def main():
    cli.main(process=args.process, single=args.single)


if __name__ == "__main__":
    main()
