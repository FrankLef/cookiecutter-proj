"""Extract XBR data from MS Access"""

# import duckdb as ddb
# from src.s0_helpers.richtools import progress_bar
from config import settings

import src.s0_helpers.richtools as rt
from src.inst_acc import main as inst_acc

duckdb_path = settings.paths.duckdb


def main() -> int:
    accdb = inst_acc(db_choice="db")
    conn = accdb[0]
    check = conn.test_connect()
    if check:
        msg: str = f"MS Access connect is ok.\n{accdb[1]}"
        rt.print_msg(msg, type="info")
    return 0


if __name__ == "__main__":
    main()
