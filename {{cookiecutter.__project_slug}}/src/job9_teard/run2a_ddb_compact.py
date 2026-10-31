# mypy: ignore-errors
"""Compacting duckdb database by copying."""

from rich import print as rprint
from config import settings
from fltk.ddb import compact_ddb


def main(is_skipped: bool = False) -> None:
    if is_skipped:
        raise NotImplementedError(f"Skip the '{__name__}' script.")
    rprint(f"Executing the '{__name__}' script.")

    compact_ddb.main(duckdb_path=settings.DDB_PATH)


if __name__ == "__main__":
    main()
