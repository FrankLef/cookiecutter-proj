"""The main entry point."""
import logging
from enum import Enum

import typer
from rich.logging import RichHandler
from src.etl.main import run_etl as etl


logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
log = logging.getLogger("rich")


class Step(Enum):
    ETL = "etl"


def main(process: str, single: bool = True) -> str:
    """Dispatch the main processes.

    Args:
        process (str): Must be in ["etl"].
        single (bool): True: It is a single step. Not currently used.

    Raises:
        ValueError: The process name is invalid.

    Returns:
        str: The value of `process`.
    """
    log.info("Run '%s' with single = %s.", process, single)
    match process:
        case Step.ETL.value:
            size: int = 5
            seed: int = 1009
            a_url = r"https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv"  # noqa: E501
            etl(size=size, seed=seed, url=a_url)
        case _:
            msg = f"'{process}' is an invalid process."
            log.error(msg)
            raise ValueError(msg)
    return process


if __name__ == "__main__":
    typer.run(main)
