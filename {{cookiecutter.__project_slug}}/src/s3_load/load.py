"""Upload to an external database."""

import importlib
from pathlib import Path

from src.s0_helpers.richtools import print_modul


def main(subproc: str | None = None, pkg_pat: str = "load*_*.py") -> int:
    wd = Path(__file__).parent
    names = sorted([f.stem for f in wd.glob(pkg_pat) if f.is_file()])
    pkg = Path(__file__).parent.name
    n: int = 0
    for nm in names:
        modul = importlib.import_module(name="." + nm, package=pkg)
        print_modul(modul)
        n += modul.main(subproc)
    return n
