# mypy: ignore-errors
"""Create the specs master used by the project."""

from config import settings

from fltk.specs.load_specs import load_specs

data_path = settings.paths.data

specs_mstr = load_specs("todo", path=data_path)
