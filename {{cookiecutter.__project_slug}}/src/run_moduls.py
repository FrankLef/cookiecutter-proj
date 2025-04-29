"""Run the modules in the src folder dynamically."""

from importlib import import_module
from pathlib import Path
from typing import Final, Any
import re
import winsound

from src.s0_helpers.richtools import print_msg, print_modul


def play_note(song: str, duration: int = 500, wake: bool = True) -> str:
    """Play a sequence of notes."""
    assert len(song) != 0, "The song must have at least one note."
    notes = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
    if wake:
        # NOTE: Windows sound are inconsistent from computer to computer
        # to ensure the first note plays, play a system sound before the song
        winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
    for note in song.upper().split():
        freq = int(256 * (2 ** (notes[note] / 12)))
        winsound.Beep(frequency=freq, duration=duration)
    return song


def run_modul(dir: str, pat: str) -> int:
    """Process the modules in the src directory with given pattern."""
    wd = Path(__file__).parent.joinpath(dir)
    if wd.exists():
        files = [item for item in wd.iterdir() if item.is_file()]
    else:
        raise NotADirectoryError(f"Invalid path\n{wd}")
    names = sorted([fn.stem for fn in files if re.match(pat, fn.name)])
    if not len(names):
        raise ValueError(f"No module found in\n{wd}")
    n: int = 0
    for nm in names:
        modul = import_module(name="." + nm, package=dir)
        print_modul(modul)
        try:
            n += modul.main()
        except TypeError:
            msg = f"The return value from '{nm}' must be an integer."
            raise TypeError(msg)
    return n


def get_pattern(suffix: str, pat: str | None = None) -> str:
    """Create the regex pattern used to filter the files."""
    if pat is None:
        pat = suffix + r".+_.*" + "[.]py"
    else:
        pat = suffix + r".+_" + pat + "[.]py"
    return pat


def get_specs(job: str | None = None) -> Any:
    """Get the procedure's specs."""
    MODULS: Final[dict[str, tuple[str, ...]]] = {
        "ex": ("extr", "s1_extr", "C"),
        "tr": ("transf", "s2_transf", "D"),
        "lo": ("load", "s3_load", "E"),
        "ra": ("raw", "s4_raw", "F"),
        "pp": ("pproc", "s5_pproc", "G"),
        "ed": ("eda", "s6_eda", "A"),
        "fi": ("final", "s7_final", "B"),
    }
    if job is not None:
        out = MODULS[job]  # type: ignore
    else:
        out = MODULS  # type: ignore
    return out


def run_job(job: str, pat: str | None = None, is_silent: bool = False) -> int:
    """Execute a single job."""
    specs = get_specs(job=job)
    pat = get_pattern(suffix=specs[0], pat=pat)
    n = run_modul(dir=specs[1], pat=pat)
    if not is_silent:
        play_note(song=specs[2])
    return n


def get_jobs(jobs: str) -> list[str]:
    """Get the oredered list of jobs."""
    jobs_list = get_specs().keys()

    # remove all whitspace, tab, newline, etc
    jobs = re.sub(r"\s+", "", jobs)

    if jobs:
        jobs_todo = jobs.lower().split(sep=",")
        jobs_todo = [x[:2] for x in jobs_todo]
        njobs_todo = len(jobs_todo)
        if njobs_todo <= len(jobs_list):
            err_nb = sum([x not in jobs_list for x in jobs_todo])
            if err_nb:
                msg = f"There are {err_nb} invalid jobs in '{jobs_todo}'.\nThe job's first 2 characters must be in {jobs_list}."
                raise KeyError(msg)
        else:
            msg = f"There are {jobs_todo} jobs to do. There must be no more than {len(jobs_list)}."
            raise IndexError(msg)
    else:
        raise ValueError("The `jobs` are empty.")
    assert len(jobs_todo) != 0, "No jobs. This should not reach this point!"
    # reorder the list to match the fixed jobs list
    jobs_todo = [x for x in jobs_list if x in jobs_todo]
    return jobs_todo


def main(jobs: str, pat: str | None = None) -> int:
    jobs_todo = get_jobs(jobs=jobs)
    print_msg(f"Processing {len(jobs)} jobs_todo \u2026", type="process")
    n: int = 0
    for job in jobs_todo:
        n += run_job(job=job, pat=pat)
    return n
