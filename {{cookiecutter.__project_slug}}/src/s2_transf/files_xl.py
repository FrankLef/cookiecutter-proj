import logging
from pathlib import Path
from time import gmtime, perf_counter, strftime

import pandas as pd
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
log = logging.getLogger("rich")


def rbind_bv(
    file: str, in_path: Path, out_path: Path, select: list[str] | None = None
) -> pd.DataFrame:
    start = perf_counter()
    out_fn = out_path.joinpath(file)
    log.info("rbind_bv files from\n%s\nto\n%s", in_path, out_fn)
    if select is None:
        dfs = [pd.read_excel(f) for f in in_path.glob("*.xlsx") if f.is_file()]
    else:
        dfs = []
        for f in in_path.glob("*.xlsx"):
            for ws_nm in select:
                dfs.append(pd.read_excel(f, sheet_name=ws_nm))
    n = len(dfs)
    if not n:
        msg = f"No file found by rbind in\n{in_path}."
        log.critical(msg)
        raise AssertionError(msg)
    df = pd.concat(dfs, ignore_index=True)
    df.to_excel(out_fn, index=False)
    t = strftime("Elapsed time %H:%M:%S.", gmtime(perf_counter() - start))
    log.info("rbind_bv %d files. %s", n, t)
    return df


def melt_bv(in_file: Path, out_file: Path, id_vars: list[str]) -> pd.DataFrame:
    start = perf_counter()
    log.info("melt_bv from\n%s\nto\n%s", in_file, out_file)
    df = pd.read_excel(in_file)
    df = df.melt(id_vars=id_vars, var_name="month_tag", value_name="amt")
    df.to_excel(excel_writer=out_file, index=False)
    t = strftime("Elapsed time %H:%M:%S.", gmtime(perf_counter() - start))
    log.info("melt_bv completed. %s", t)
    return df
