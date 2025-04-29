"""Main CLI entry point."""

from typing import Final
import typer
# import importlib
# import winsound

from .run_moduls import main as run_cmd
from src.s0_helpers.richtools import print_msg

app = typer.Typer()


@app.command()
def pipe(tasks: str, pat: str | None = None) -> int:
    """Run a pipe of commands.

    The `tasks` argument is a comma-separated string with the task ids. Task ids must be one of 'ex', 'tr', 'lo', 'ra', 'pp', 'ed', 'fi'. For example, you can use 'ex,tr' for 'extract' then 'transform'. The order does not matter.
    The `tasks` is case-insensitive. All spaces are removed. The task id could be any word as long as it starts with the proper two letter. For example 'transform_it, EXT' is the same as 'ex,tr'.  If a task appears more that once, it will be processed only once.

    Args:
        tasks (str): comma-separated string with the task.
        pat (str | None, optional): Patttern passed on to the command to fitler files. Defaults to None.

    Raises:
        KeyError: There are invalid task id.
        IndexError: There are too many tasks.
        ValueError: The `tasks` argument is empty.

    Returns:
        int: The sum of all the integers returned by the tasks.
    """
    SEP: Final[str] = ","
    TASKS: Final[tuple[str, ...]] = ("ex", "tr", "lo", "ra", "pp", "ed", "fi")

    tasks = tasks.replace(" ", "")

    if tasks:
        tasks_todo = tasks.lower().split(sep=SEP)
        tasks_todo = [x[:2] for x in tasks_todo]
        ntasks_todo = len(tasks_todo)
        if ntasks_todo <= len(TASKS):
            err_nb = sum([x not in TASKS for x in tasks_todo])
            if err_nb:
                msg = f"There are {err_nb} invalid tasks in '{tasks}'.\nThe task first 2 characters must be in {TASKS}."
                raise KeyError(msg)
        else:
            msg = f"There are {ntasks_todo} tasks. There must be no more than {len(TASKS)}."
            raise IndexError(msg)
    else:
        raise ValueError("The `tasks` argument must be provided.")

    print_msg(f"Processing {ntasks_todo} main tasks \u2026", type="process")
    n: int = 0
    # NOTE: run the command in the pre-determined order
    for proc in TASKS:
        if proc in tasks_todo:
            n += run_cmd(proc=proc, pat=pat)
    return n


@app.command()
def extr(pat: str | None = None) -> int:
    """Extract data from an external source.

    Args:
        pat (str | None, optional): Patttern passed on to the command to fitler files. Defaults to None.

    Returns:
        int: Integer returned by the process.
    """
    n = run_cmd(proc="extr", pat=pat)
    return n


@app.command()
def transf(pat: str | None = None) -> int:
    """Tranform the extracted data to a table format.

    Args:
        pat (str | None, optional): Patttern passed on to the command to fitler files. Defaults to None.

    Returns:
        int: Integer returned by the process.
    """
    n = run_cmd(proc="transf", pat=pat)
    return n


@app.command()
def load(pat: str | None = None) -> int:
    """Upload to an external database.

    Args:
        pat (str | None, optional): Patttern passed on to the command to fitler files. Defaults to None.

    Returns:
        int: Integer returned by the process.
    """
    n = run_cmd(proc="load", pat=pat)
    return n


@app.command()
def raw(pat: str | None = None) -> int:
    """Get raw data for EDA.

    Args:
        pat (str | None, optional): Patttern passed on to the command to fitler files. Defaults to None.

    Returns:
        int: Integer returned by the process.
    """
    n = run_cmd(proc="raw", pat=pat)
    return n


@app.command()
def pproc(pat: str | None = None) -> int:
    """Preprocess data for EDA.

    Args:
        pat (str | None, optional): Patttern passed on to the command to fitler files. Defaults to None.

    Returns:
        int: Integer returned by the process.
    """
    n = run_cmd(proc="pproc", pat=pat)
    return n


@app.command()
def eda(pat: str | None = None) -> int:
    """Exploratory Data Analysis.

    Args:
        pat (str | None, optional): Patttern passed on to the command to fitler files. Defaults to None.

    Returns:
        int: Integer returned by the process.
    """
    n = run_cmd(proc="eda", pat=pat)
    return n


@app.command()
def final(pat: str | None = None) -> int:
    """Finalize EDA.

    Args:
        pat (str | None, optional): Patttern passed on to the command to fitler files. Defaults to None.

    Returns:
        int: Integer returned by the process.
    """
    n = run_cmd(proc="final", pat=pat)
    return n


if __name__ == "__main__":
    app()
