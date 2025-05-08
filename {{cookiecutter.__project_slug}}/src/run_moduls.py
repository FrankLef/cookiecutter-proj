"""Run the modules in the src folder dynamically."""

from importlib import import_module
from pathlib import Path
from dataclasses import dataclass, field

# from rich.pretty import pprint
import re
import winsound

from src.s0_helpers.richtools import print_msg, print_modul


@dataclass
class Job:
    name: str
    suffix: str
    job_dir: str
    pattern: str | None = None
    moduls: list[str] = field(default_factory=list)
    emo: str | None = "\u2728"
    song: str = ""


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


def run_modul(job_dir: str, names: list[str]) -> int:
    """Process the modules in the src directory with given pattern."""
    n: int = 0
    for nm in names:
        modul = import_module(name="." + nm, package=job_dir)
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
        pat = "^" + suffix + r".+_.*" + "[.]py$"
    else:
        pat = "^" + suffix + r".+_" + pat + "[.]py$"
    return pat


def get_moduls(job_dir: str, pat: str) -> list[str]:
    """Get the list of modules in the given directory with the pattern.

    Args:
        job_dir (str): Job directory.
        pat (str): File pattern to use.

    Raises:
        NotADirectoryError: Invalid directory.
        ValueError: The job directory is empty.

    Returns:
        list[str]: The modules to process.
    """
    wd = Path(__file__).parent.joinpath(job_dir)
    if wd.exists():
        files = [item for item in wd.iterdir() if item.is_file()]
    else:
        raise NotADirectoryError(f"Invalid path\n{wd}")
    moduls = sorted([fn.stem for fn in files if re.match(pat, fn.name)])
    if not len(moduls):
        raise ValueError(f"No module found in\n{wd}")
    return moduls


def get_jobs(jobs: list[str] | None = None) -> dict[str, Job]:
    """Get the jobs' fixed specs.

    Args:
        jobs (list[str] | None, optional): List of jobs. Defaults to None.

    Returns:
        dict[str, Job]: Dictionnary of jobs.
    """
    all_jobs = {
        "ex": Job(
            name="Extract", suffix="extr", job_dir="s1_extr", emo="\u2728", song="C"
        ),
        "tr": Job(
            name="Transform",
            suffix="transf",
            job_dir="s2_transf",
            emo="\u2728",
            song="D",
        ),
        "lo": Job(
            name="Load", suffix="load", job_dir="s3_load", emo="\u2728", song="E"
        ),
        "ra": Job(name="Raw", suffix="raw", job_dir="s4_raw", emo="\u2728", song="F"),
        "pp": Job(
            name="Preprocess",
            suffix="pproc",
            job_dir="s5_pproc",
            emo="\u2728",
            song="G",
        ),
        "ed": Job(name="EDA", suffix="eda", job_dir="s6_eda", emo="\u2728", song="A"),
        "fi": Job(
            name="Final", suffix="final", job_dir="s7_final", emo="\u2728", song="B"
        ),
    }
    if jobs is not None:
        out = {key: all_jobs[key] for key in jobs}
    else:
        out = all_jobs
    return out


def get_jobs_todo(jobs: str) -> list[str]:
    """Get the ordered list of jobs."""
    # jobs_list = specs().keys()
    jobs_list = get_jobs().keys()

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


def get_jobs_specs(jobs: str, pat: str | None = None) -> dict[str, Job]:
    """Get the specs for the jobs todo.

    Args:
        jobs (str): String of jobs to do.
        pat (str | None, optional): Regex pattern. Defaults to None.

    Returns:
        dict[str, Job]: Dictionnary of job specs.
    """
    jobs_todo = get_jobs_todo(jobs=jobs)
    jobs_specs = get_jobs(jobs=jobs_todo)
    print_msg(f"Processing {len(jobs_todo)} jobs \u2026", type="process")
    # populate the job with pattern and file names
    for _, specs in jobs_specs.items():
        pat_regx = get_pattern(suffix=specs.suffix, pat=pat)
        specs.pattern = pat_regx
        moduls = get_moduls(job_dir=specs.job_dir, pat=specs.pattern)
        specs.moduls = moduls
        # pprint(specs)
    return jobs_specs


def main(jobs: str, pat: str | None = None, is_silent: bool = True) -> int:
    jobs_specs = get_jobs_specs(jobs=jobs, pat=pat)
    moduls_count = sum([len(x.moduls) for x in jobs_specs.values()])
    print_msg(f"Processing {moduls_count} modules \u2026", type="process")
    n: int = 0
    for specs in jobs_specs.values():
        msg = f"Run the {specs.name} modules. {specs.emo}"
        print_msg(msg, type="process")
        n += run_modul(job_dir=specs.job_dir, names=specs.moduls)
        if not is_silent:
            play_note(song=specs.song)
    return n
