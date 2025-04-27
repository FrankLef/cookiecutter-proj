"""Extract data from external source."""

import importlib
from pathlib import Path

import src.s0_helpers.richtools as rt


def main(pat: str | None = None) -> int:
    stem = "extr*_*"
    if pat is None:
        pat = stem + ".py"
    else:
        pat = stem + pat + ".py"
    pkg = Path(__file__).parent.name
    wd = Path(__file__).parent
    names = sorted([f.stem for f in wd.glob(pat) if f.is_file()])
    n: int = 0
    for nm in names:
        modul = importlib.import_module(name="." + nm, package=pkg)
        rt.print_modul(modul)
        try:
            n += modul.main()
        except TypeError:
            msg = f"The return value from '{nm}' must be an integer."
            raise TypeError(msg)
    return n
