"""Main CLI entry point."""

import typer
import importlib
import winsound

from src.s0_helpers.richtools import print_msg, print_modul

app = typer.Typer()


def play_note(song: str, duration: int = 500, wake: bool = True):
    """Play a sequence of notes."""
    assert len(song) != 0, "The song must have at keast one note."
    notes = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
    if wake:
        # NOTE: Windows sound are inconsistent from computer to computer
        # to ensure the first note plays, play a system sound before the song
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
    for note in song.upper().split():
        freq = int(256 * (2 ** (notes[note] / 12)))
        winsound.Beep(frequency=freq, duration=duration)


def run_cmd(proc: str, subproc: str | None = None) -> int:
    """Run the main modules.

    Args:
        proc (str): Name of the main module to run.
        subproc (str | None, optional): Name of subprocess pased on to the main module. Defaults to None.

    Returns:
        int: Integer returned by the mian module.
    """
    MODULS = {
        "extr": "s1_extr.extr",
        "transf": "s2_transf.transf",
        "load": "s3_load.load",
        "raw": "s4_raw.raw",
        "pproc": "s5_pproc.pproc",
        "eda": "s6_eda.eda",
        "final": "s7_final.final",
    }

    modul_nm = MODULS[proc]
    modul = importlib.import_module(name=modul_nm)
    print_modul(modul)
    n = modul.main(subproc)
    return n


@app.command()
def pipe(tasks: str, subproc: str | None = None) -> int:
    """Run a pipe of commands.

    The `tasks` argument is a comma-separated string with the task ids. Task ids must be one of 'ex', 'tr', 'lo', 'ra', 'pp', 'ed', 'fi'. For example, you can use 'ex,tr' for 'extract' then 'transform'. The order does not matter.
    The `tasks` is case-insensitive. All spaces are removed. The task id could be any word as long as it starts with the proper two letter. For example 'transform_it, EXT' is the same as 'ex,tr'.  If a task appears more that once, it will be processed only once.

    Args:
        tasks (str): comma-separated string with the task.
        subproc (str | None, optional): Subprocess pased on to the command.. Defaults to None.

    Raises:
        KeyError: There are invalid task id.
        IndexError: There are too many tasks.
        ValueError: The `tasks` argument is empty.

    Returns:
        int: The sum of all the integers returned by the tasks.
    """
    SEP: str = ","
    TASKS = {
        "ex": "extr",
        "tr": "transf",
        "lo": "load",
        "ra": "raw",
        "pp": "pproc",
        "ed": "eda",
        "fi": "final",
    }

    tasks = tasks.replace(" ", "")

    if tasks:
        tasks_todo = tasks.lower().split(sep=SEP)
        tasks_todo = [x[:2] for x in tasks_todo]
        ntasks_todo = len(tasks_todo)
        if ntasks_todo <= len(TASKS):
            err_nb = sum([x not in TASKS.keys() for x in tasks_todo])
            if err_nb:
                msg = f"There are {err_nb} invalid tasks in '{tasks}'.\nThe task first 2 characters must be in {TASKS.keys()}."
                raise KeyError(msg)
        else:
            msg = f"There are {ntasks_todo} tasks. There must be no more than {len(TASKS)}."
            raise IndexError(msg)
    else:
        raise ValueError("The `tasks` argument must be provided.")

    # run the command in the order in which they are in the tasks dictionary
    print_msg(f"Processing {ntasks_todo} main tasks \u2026", type="process")
    n: int = 0
    for key, val in TASKS.items():
        if key in tasks_todo:
            n += run_cmd(proc=val, subproc=subproc)
    play_note(song="E C")
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
