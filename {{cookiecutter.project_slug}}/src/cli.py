"""Dispatch the command received from the entry point."""
import logging

from rich.logging import RichHandler
from etl.main import run_etl as etl
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
log = logging.getLogger("rich")


def main(process: str, single: bool) -> int:
    log.info("Run '%s' with single = %s.", process, single)
    size: int = 5
    seed: int = 1009
    a_url = r"https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv"  # noqa: E501
    etl(size=size, seed=seed, url=a_url)
    return -1
