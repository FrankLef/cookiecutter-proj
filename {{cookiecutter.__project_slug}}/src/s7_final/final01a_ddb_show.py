"""Show database info"""

import duckdb as ddb
import src.s0_helpers.richtools as rt

from config import settings

duckdb_path = settings.duck_db.fn


def main() -> int:
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
