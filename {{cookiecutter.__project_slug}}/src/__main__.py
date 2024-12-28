"""Main CLI entry point."""

import typer
import importlib

from src.s0_helpers.richtools import print_modul

app = typer.Typer()

the_moduls = {
    "extr": "s1_extr.extr",
    "transf": "s2_transf.transf",
    "load": "s3_load.load",
    "raw": "s4_raw.raw",
    "pproc": "s5_pproc.pproc",
    "eda": "s6_eda.eda",
    "final": "s7_final.final",
}


def run_cmd(proc: str, subproc: str | None = None) -> int:
    """Use this to run the primary modules."""
    modul_nm = the_moduls[proc]
    modul = importlib.import_module(name=modul_nm)
    print_modul(modul)
    n = modul.main(subproc)
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
