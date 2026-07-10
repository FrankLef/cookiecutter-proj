# mypy: ignore-errors
"""Create Dicz."""

from config import settings

from fltk.dicz.create_dicz import create_dicz

data_path = settings.paths.data

dicz = create_dicz(key="example", path=data_path)
