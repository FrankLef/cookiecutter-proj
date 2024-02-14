"""The main entry point."""
import argparse
import logging
import cli
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
log = logging.getLogger("rich")

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
    log.info("Begin the process.")
    log.debug("process: '%s', single: %s.", args.process, args.single)
    cli.main(process=args.process, single=args.single)
    log.info("End the process.")


if __name__ == "__main__":
    main()
