"""Export files to reports."""

import shutil
from rich import print as rprint
from typing import NamedTuple
from pathlib import Path

from config import settings

path_transf = settings.paths.data_transf
path_raw = settings.paths.data_raw
path_pproc = settings.paths.data_pproc
path_eda = settings.paths.data_eda
path_reports = settings.paths.reports_data

class XprtFile(NamedTuple):
    name: str
    skip: bool = False

class XprtDir(NamedTuple):
    name: str
    path: Path
    files: list[XprtFile]
    
xprt_transf = XprtDir(
    name="transf",
    path=path_transf,
    files=[
        XprtFile(name="clus_client_3D.html"),
        XprtFile(name="clus_client_bubbles.html", skip=True),
        XprtFile(name="clus_genus_3D.html", skip=False),
    ]
)

xprt_raw = XprtDir(
    name="raw",
    path=path_raw,
    files=[
        XprtFile(name="catfr_crosstabl.html"),
        XprtFile(name="clus_crosstabl.html", skip=True),
    ]
)

xprt_pproc = XprtDir(
    name="pproc",
    path=path_pproc,
    files=[
        XprtFile(name="mba_tabl.html", skip=False),
    ]
)

xprt_eda = XprtDir(
    name="eda",
    path=path_eda,
    files=[
        XprtFile(name="elast_catfr.html"),
        XprtFile(name="elast_genus.html", skip=True),
    ]
)

xprts = [xprt_transf, xprt_raw, xprt_pproc, xprt_eda]

def export_files(xprt: XprtDir, path: Path) -> int:
    nfiles: int = 0
    msg = f"Exporting from\n{xprt.path}\nto\n{path}"
    rprint(msg)
    for a_file in xprt.files:
        if not a_file.skip:
            rprint(f"'{a_file.name}'")
            src_fn = xprt.path.joinpath(a_file.name)
            dest_fn = path.joinpath(a_file.name)
            shutil.copy2(src=src_fn, dst=dest_fn)
            nfiles += 1
    if not nfiles:
        msg = f"No file exported from '{xprt.name}'."
        rprint(msg)
    return nfiles


def main(is_skipped: bool = True) -> None:
    if is_skipped:
        raise NotImplementedError(f"Skip the '{__name__}' script.")
    
    if len(xprts):
        for xprt in xprts:
            nfiles = export_files(xprt, path=path_reports)
            msg = f"{nfiles} files exported from '{xprt.name}'."
            rprint(msg)
    else:
        raise ValueError("No file to export.")
