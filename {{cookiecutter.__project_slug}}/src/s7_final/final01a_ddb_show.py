"""Show database info"""

import warnings
import duckdb as ddb
import src.s0_helpers.richtools as rt

from config import settings

duckdb_path = settings.duck_db.fn


def main(is_skipped: bool = True) -> int:
    """Main function.

    Args:
        is_skipped (bool, optional): Skip this module if True. Defaults to False.

    Returns:
        int: Return an integer on the status.
    """
    if is_skipped:
        msg = f"{__file__} is skipped."
        warnings.warn(msg, category=UserWarning)
        return 0
    with ddb.connect(duckdb_path) as conn:
        conn.sql("DESCRIBE TABLES").show()
        data = conn.sql("DESCRIBE TABLES").fetchall()
        tbls = [x[0] for x in data]
        for tbl in tbls:
            rt.print_msg(tbl, type="info")
            conn.sql(f"DESCRIBE {tbl}").show()
    return 1


if __name__ == "__main__":
    main()
