"""Create the connection to MS Access used by the project."""

from pathlib import Path

from fltk.conn.connect_acc import ConnectAcc


def acc_conn(db_choice: str = "main") -> ConnectAcc:
    paths = {
        "main": Path(
            "C:/Users/Public/MyJob/DesjCap_cies/springfree1a/springfree1a.accdb"
        ),
        "raw": Path(
            "C:/Users/Public/MyJob/DesjCap_cies/springfree1a/springfree1a.accdb"
        ),
        "xbr": Path("C:/Users/Public/MyAcctg/xbrl/db_xbr.accdb"),
    }
    try:
        path = paths[db_choice]
    except KeyError as e:
        msg: str = f"'{db_choice}' is an invalid MS Access choices."
        e.add_note(msg)
        raise
    conn = ConnectAcc(path=path)
    return conn


ACC_CONN = acc_conn
