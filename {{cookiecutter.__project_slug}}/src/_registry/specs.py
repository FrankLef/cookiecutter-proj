# mypy: ignore-errors
"""Create the specs master used by the project."""

from config import settings
from fltk.specs.load_specs import load_specs

specs_mstr = load_specs(settings.SPECS_NAME, path=settings.SPECS_DIR)
