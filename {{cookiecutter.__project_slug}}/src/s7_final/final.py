"""Finalize EDA."""

import importlib
from pathlib import Path

import src.s0_helpers.richtools as rt


def main(subproc: str | None = None) -> int:
    PAT = "final*_*.py"
    pkg = Path(__file__).parent.name
    wd = Path(__file__).parent
    names = sorted([f.stem for f in wd.glob(PAT) if f.is_file()])
    n: int = 0
    for nm in names:
        modul = importlib.import_module(name="." + nm, package=pkg)
        rt.print_modul(modul)
        n += modul.main(subproc)
    return n
