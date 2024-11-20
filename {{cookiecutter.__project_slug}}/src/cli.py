"""The main entry point."""

# ruff: noqa: E402

import logging
import sys
from pathlib import Path

import typer
from rich.logging import RichHandler

from extr.extract import main as extr  # type: ignore
from transf.transform import main as transf  #  type: ignore
from load.load import main as load_db  # type: ignore


src_path = Path(__file__).parent
if src_path not in sys.path:
    sys.path.insert(1, str(src_path))

proj_path = Path(__file__).parents[1]
if proj_path not in sys.path:
    sys.path.insert(1, str(proj_path))

from config import settings  # type: ignore

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
log = logging.getLogger("rich")

app = typer.Typer()

data_path = settings.paths.data
tdict_path = settings.tdict
tdict_path = data_path.joinpath(tdict_path)

if tdict_path.is_file():
    print(tdict_path)
else:
    raise FileNotFoundError(f"File not found: {tdict_path}")

@app.command()
def extract(subprocess: str) -> int:
    """Extract data.

    Args:
        subprocess (str): Must be in ['conso', 'test'].

    Returns:
        int: Number of files processed.
    """
    if subprocess in ["conso", "test"]:
        n = extr(subprocess)
    else:
        msg = f"'{subprocess}' is an invalid extract `subprocess`."
        log.error(msg)
        raise ValueError(msg)
    return n


@app.command()
def transform(subprocess: str) -> int:
    """Transform data.

    Args:
        subprocess (str): Must be in ['conso', 'test'].

    Returns:
        int: Number of files processed.
    """
    if subprocess in ["conso", "test"]:
        n = transf(subprocess)
    else:
        msg = f"'{subprocess}' is an invalid transform `subprocess`."
        log.error(msg)
        raise ValueError(msg)
    return n


@app.command()
def load(subprocess: str) -> int:
    """Load budget data to MS Access.

    Args:
        subprocess (str): Must be in ['conso', 'test'].

    Returns:
        int: Number of files processed.
    """
    if subprocess in ["conso", "test"]:
        n = load_db(subprocess)
    else:
        msg = f"'{subprocess}' is an invalid load `subprocess`."
        log.error(msg)
        raise ValueError(msg)
    return n


if __name__ == "__main__":
    app()
