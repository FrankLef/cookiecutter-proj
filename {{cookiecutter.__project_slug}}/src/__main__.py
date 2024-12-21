"""Main entry point."""

# ruff: noqa: E402

import logging

import typer
from rich.logging import RichHandler

from config import settings

from s1_extr.extr import main as do_extr
from s2_transf.transf import main as do_transf
from s3_load.load import main as do_load


logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
log = logging.getLogger("rich")

app = typer.Typer()


@app.command()
def extract(subprocess: str) -> int:
    """Extract data from external source.

    Args:
        subprocess (str): Must be in ['test'].

    Returns:
        int: Number of files processed.
    """
    if subprocess in ["test"]:
        n = do_extr(subprocess)
    else:
        msg = f"'{subprocess}' is an invalid extract `subprocess`."
        log.error(msg)
        raise ValueError(msg)
    return n


@app.command()
def transform(subprocess: str) -> int:
    """Transform data.

    Args:
        subprocess (str): Must be in ['test'].

    Returns:
        int: Number of files processed.
    """
    if subprocess in ["test"]:
        n = do_transf(subprocess)
    else:
        msg = f"'{subprocess}' is an invalid transform `subprocess`."
        log.error(msg)
        raise ValueError(msg)
    return n


@app.command()
def load(subprocess: str) -> int:
    """Upload data to database.

    Args:
        subprocess (str): Must be in ['test'].

    Returns:
        int: Number of files processed.
    """
    if subprocess in ["test"]:
        n = do_load(subprocess)
    else:
        msg = f"'{subprocess}' is an invalid load `subprocess`."
        log.error(msg)
        raise ValueError(msg)
    return n


if __name__ == "__main__":
    app()
