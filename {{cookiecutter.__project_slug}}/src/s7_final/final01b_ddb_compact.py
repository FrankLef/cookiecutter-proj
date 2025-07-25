"""Compacting duckdb database by copying."""

# source:
# https://duckdb.org/docs/operations_manual/footprint_of_duckdb/reclaiming_space
import warnings
import duckdb
# import sys
# from pathlib import Path

from config import settings  # noqa:E402

duckdb_path = settings.duckdb
try:
    temp_path = duckdb_path.joinpath("temp.duckdb")
except AttributeError:
    msg = "temp path is str type because the duckdb path is invalid."
    raise AttributeError(msg)


def copy_db():
    """Copy the database."""
    try:
        temp_path.unlink()
    except FileNotFoundError:
        pass
    qry = (
        f"ATTACH '{duckdb_path}' AS db1;"
        f"ATTACH '{temp_path}' AS db2;"
        f"COPY FROM DATABASE db1 to db2;"
    )
    duckdb.execute(qry)
    qry = "DETACH db1;DETACH db2;"
    duckdb.execute(qry)


def ren_db():
    """Rename the database."""
    new_path = temp_path.with_name(duckdb_path.name)
    duckdb_path.unlink()
    temp_path.replace(new_path)


def test_db(tbl: str = "trialbal"):
    """Test the compacted database."""
    with duckdb.connect(duckdb_path) as conn:
        data = conn.sql("DESCRIBE TABLES").fetchall()
        print(f"{len(data)} tables in '{duckdb_path.name}'.")


def main(is_skipped: bool = True):
    """Main function.

    Args:
        is_skipped (bool, optional): Skip this module if True. Defaults to False.

    Returns:
        int: Return an integer on the status.
    """
    if is_skipped:
        msg = f"{__name__} is skipped."
        warnings.warn(msg, category=UserWarning)
        return 0
    print(f"Compacting {duckdb_path}.")
    copy_db()
    ren_db()
    test_db()
    return 1


if __name__ == "__main__":
    main()
