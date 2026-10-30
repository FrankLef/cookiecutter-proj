# mypy: ignore-errors
"""Create the specs master used by the project."""

from pathlib import Path
from fltk.specs.load_specs import load_specs

specs_mstr = load_specs("todo", path=Path(__file__).parents[1].joinpath("_specs"))
