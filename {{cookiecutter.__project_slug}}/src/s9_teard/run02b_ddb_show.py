"""Show database info."""

import duckdb as ddb
from rich import print as rprint

from config import settings

duckdb_path = settings.paths.duckdb


def main() -> None:
    with ddb.connect(duckdb_path) as conn:
        conn.sql("DESCRIBE TABLES").show()
        data = conn.sql("DESCRIBE TABLES").fetchall()
        tbls = [x[0] for x in data]
        for tbl in tbls:
            rprint(tbl)
            conn.sql(f"DESCRIBE {tbl}").show()


if __name__ == "__main__":
    main()
