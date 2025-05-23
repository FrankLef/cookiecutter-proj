"""Export files to reports."""

import warnings
import shutil
from rich import print as rprint

from config import settings

path_transf = settings.paths.data_transf
path_raw = settings.paths.data_raw
path_reports = settings.paths.data_reports


def get_xprt():
    """Define the dictionary of files to export."""
    out = {
        "transf": {"path": path_transf, "files": ("dendo.png", "hclus_var.html")},
        "raw": {
            "path": path_raw,
            "files": (
                "clus_dist_A.html",
                "clus_dist_B.html",
                "clus_dist_C.html",
                "clus_dist_D.html",
            ),
        },
    }
    return out


def main(is_skipped: bool = True) -> int:
    """Main function.

    Args:
        is_skipped (bool, optional): Skip this module if True. Defaults to False.

    Returns:
        int: Return an integer on the status.
    """
    if is_skipped:
        warnings.warn(f"{__name__} is skipped.", category=UserWarning)
        return 0
    xprt = get_xprt()
    if not len(xprt):
        raise ValueError("No file to export.")
    n: int = 0
    for key, val in xprt.items():
        src_path = val["path"]
        files = val["files"]
        msg = f"'{key}': Exporting {len(files)} files from\n{src_path}\nto\n{path_reports}"
        rprint(msg)
        for fn in files:
            src_fn = src_path.joinpath(fn)
            dest_fn = path_reports.joinpath(fn)
            # use copy2() to keep the metadata (e.g. date)
            shutil.copy2(src=src_fn, dst=dest_fn)
            n += 1
    return n
