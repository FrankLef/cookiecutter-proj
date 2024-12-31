"""Main CLI entry point."""

import typer
import importlib

from pkrl import main as utils
from src.s0_helpers.richtools import print_msg, print_modul

app = typer.Typer()

MODULS = {
    "extr": "s1_extr.extr",
    "transf": "s2_transf.transf",
    "load": "s3_load.load",
    "raw": "s4_raw.raw",
    "pproc": "s5_pproc.pproc",
    "eda": "s6_eda.eda",
    "final": "s7_final.final",
}


@app.command()
def say_hello():
    """This a test to validate the import of pkrl."""
    msg = utils.hello()
    return msg


def run_cmd(proc: str, subproc: str | None = None) -> int:
    """Run the main modules.

    Args:
        proc (str): Name of the main module to run.
        subproc (str | None, optional): Name of subprocess pased on to the main module. Defaults to None.

    Returns:
        int: Integer returned by the mian module.
    """
    
    modul_nm = MODULS[proc]
    modul = importlib.import_module(name=modul_nm)
    print_modul(modul)
    n = modul.main(subproc)
    return n

@app.command()
def pipe(tasks: str, subproc: str | None = None) -> int:
    """Run a pipe of commands.
    
    The `tasks` argument is '|'-separated string with the task ids. Task id must be one of 'ex', 'tr', 'lo', 'ra', 'pp', 'ed', 'fi'. For example, you
    can use 'ex|tr' for 'extract' then 'transform'. The order does not matter.
    The `tasks` is case-insensitive. The task id could be any word as long as it starts with the proper to letter. For example 'transform_is|EXT' is the
    same as 'ex|tr'.  If a task appear more that once, it will be processed only once.

    Args:
        tasks (str): '|'-separated string with the task.
        subproc (str | None, optional): Subprocess pased on to the command.. Defaults to None.

    Raises:
        ValueError: There are invalid task id.
        ValueError: The `tasks` argument is empty.

    Returns:
        int: The sum of all the integers returned by the tasks.
    """
    SEP: str = ','
    TASKS = {
        'ex': 'extr',
        'tr': 'transf',
        'lo': 'load',
        'ra': 'raw',
        'pp': 'pproc',
        'ed': 'eda',
        'fi': 'final'
    }
    
    if tasks:
        tasks_todo = tasks.split(sep=SEP)
        tasks_todo = [x.lower()[:2] for x in tasks_todo]
        err_nb = sum([x not in TASKS.keys() for x in tasks_todo])
        if err_nb:
            msg = f"There are {err_nb} invalid tasks in '{tasks}'.\nThe task first 2 characters must be in {TASKS.keys()}."
            raise ValueError(msg)
    else:
        raise ValueError("The `tasks` argument must be provided.")
    
    # run the command in the order in which they are in the tasks dictionary
    print_msg(f"Processing {len(tasks_todo)} tasks \u2026", type = "process")
    n: int = 0
    for key, val in TASKS.items():
        if key in tasks_todo:
            n += run_cmd(proc=val, subproc=subproc)
    
    return n



@app.command()
def extr(subproc: str | None = None) -> int:
    """Extract data from an external source.

    Args:
        subproc (str | None, optional): Name of the subprocess. Defaults to None.

    Returns:
        int: Integer returned by the process.
    """
    n = run_cmd(proc="extr", subproc=subproc)
    return n


@app.command()
def transf(subproc: str | None = None) -> int:
    """Tranform the extracted data to a table format.

    Args:
        subproc (str | None, optional): Name of the subprocess. Defaults to None.

    Returns:
        int: Integer returned by the process.
    """
    n = run_cmd(proc="transf", subproc=subproc)
    return n


@app.command()
def load(subproc: str | None = None) -> int:
    """Upload to an external database.

    Args:
        subproc (str | None, optional): Name of the subprocess. Defaults to None.

    Returns:
        int: Integer returned by the process.
    """
    n = run_cmd(proc="load", subproc=subproc)
    return n


@app.command()
def raw(subproc: str | None = None) -> int:
    """Get raw data for EDA.

    Args:
        subproc (str | None, optional): Name of the subprocess. Defaults to None.

    Returns:
        int: Integer returned by the process.
    """
    n = run_cmd(proc="raw", subproc=subproc)
    return n


@app.command()
def pproc(subproc: str | None = None) -> int:
    """Preprocess data for EDA.

    Args:
        subproc (str | None, optional): Name of the subprocess. Defaults to None.

    Returns:
        int: Integer returned by the process.
    """
    n = run_cmd(proc="pproc", subproc=subproc)
    return n


@app.command()
def eda(subproc: str | None = None) -> int:
    """Exploratory Data Analysis.

    Args:
        subproc (str | None, optional): Name of the subprocess. Defaults to None.

    Returns:
        int: Integer returned by the process.
    """
    n = run_cmd(proc="eda", subproc=subproc)
    return n


@app.command()
def final(subproc: str | None = None) -> int:
    """Finalize EDA.

    Args:
        subproc (str | None, optional): Name of the subprocess. Defaults to None.

    Returns:
        int: Integer returned by the process.
    """
    n = run_cmd(proc="final", subproc=subproc)
    return n


if __name__ == "__main__":
    app()
