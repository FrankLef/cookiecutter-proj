"""Run the modules in the src folder dynamically."""

from importlib import import_module
from pathlib import Path
from typing import Final
import winsound

from src.s0_helpers.richtools import print_modul


def play_note(song: str, duration: int = 500, wake: bool = True) -> None:
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


def run_proc(dir: str, pat: str) -> int:
    """Process the modules in the src directory with given pattern."""
    wd = Path(__file__).parent.joinpath(dir)
    if not wd.exists():
        raise NotADirectoryError(f"Invalid path\n{wd}")
    names = sorted([f.stem for f in wd.glob(pat) if f.is_file()])
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
    """Create the pattern for glob()"""
    stem = suffix + "*_*"
    if pat is None:
        pat = stem + ".py"
    else:
        pat = stem + pat + ".py"
    return pat


def get_specs(proc: str) -> tuple[str, ...]:
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
    specs = MODULS[proc]
    return specs


def main(proc: str, pat: str | None = None) -> int:
    specs = get_specs(proc=proc)
    pat = get_pattern(suffix=specs[0], pat=pat)
    n = run_proc(dir=specs[1], pat=pat)
    play_note(song=specs[2])
    return n
