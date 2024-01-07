"""The entry point.
"""
import argparse
import logging
from rich.logging import RichHandler

import dispatch

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
log = logging.getLogger("rich")

parser = argparse.ArgumentParser(
    prog="Hello", description="Say Hello many times.", epilog="Good luck."
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="output detailed info to the console.",
)
parser.add_argument(
    "-t",
    "--text",
    action="store",
    default="Hello",
    help="The text to show on the console.",
)
parser.add_argument(
    "text",
    action="store",
    help="The text to show on the console.",
)
parser.add_argument(
    "-n",
    "--number",
    action="store",
    default=1,
    help="The number of times we say Hello.",
)
args = parser.parse_args()


def main():
    log.info("Begin EDGAR.")
    log.debug("%s %d times.", args.text, int(args.number))
    dispatch.main(text=args.text, n=int(args.number))
    log.info("End EDGAR.")


main()
