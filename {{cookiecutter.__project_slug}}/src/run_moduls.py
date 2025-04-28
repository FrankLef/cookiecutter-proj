"""Run the modules in the src folder dynamically."""
import importlib
import winsound
from pathlib import Path
from typing import Final

from src.s0_helpers.richtools import print_modul

def play_note(song: str, duration: int = 500, wake: bool = True)->None:
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


def run_proc(dir: str, proc: str, pat: str | None = None) -> int:
    """Process the modules in the src directory."""
    stem = proc + "*_*"
    if pat is None:
        pat = stem + ".py"
    else:
        pat = stem + pat + ".py"
    wd = Path(__file__).parent.joinpath(dir)
    if not wd.exists():
        raise NotADirectoryError(f"Invalid path\n{wd}")
    names = sorted([f.stem for f in wd.glob(pat) if f.is_file()])
    if not len(names):
        raise ValueError(f"No module found in\n{wd}")
    n: int = 0
    for nm in names:
        modul = importlib.import_module(name="." + nm, package=dir)
        print_modul(modul)
        try:
            n += modul.main()
        except TypeError:
            msg = f"The return value from '{nm}' must be an integer."
            raise TypeError(msg)
    return n


def get_specs(proc: str, pat: str | None = None) -> tuple[str,str]:
    """Get the procedure's specs."""
    MODULS: Final[dict[str, tuple[str, str]]] = {
        "extr": ("s1_extr", "C"),
        "transf": ("s2_transf", "D"),
        "load": ("s3_load", "E"),
        "raw": ("s4_raw", "F"),
        "pproc": ("s5_pproc", "G"),
        "eda": ("s6_eda", "A"),
        "final": ("s7_final", "A"),
    }
    specs = MODULS[proc]
    return specs

def main(proc: str, pat: str | None = None, is_silent: bool = False) -> int:
    specs = get_specs(proc=proc, pat=pat)
    n = run_proc(dir=specs[0], proc=proc, pat=pat)
    if not is_silent:
        play_note(song=specs[1])
    return n