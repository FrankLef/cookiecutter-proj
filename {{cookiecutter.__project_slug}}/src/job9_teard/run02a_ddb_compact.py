# mypy: ignore-errors
"""Compacting duckdb database by copying."""

from rich import print as rprint
from config import settings
from fltk.ddb import compact_ddb

duckdb_path = settings.paths.duckdb


def main() -> None:

    compact_ddb.main(duckdb_path=duckdb_path)
