"""Test the MS Access connection."""

import pytest
from pathlib import Path
from sqlalchemy import engine

import src.etl.extract_acc as extr


@pytest.fixture
def db_path(
    file: str = r"C:\Users\Public\MyJob\DesjCap_cies\NSE\OlapNse_V02\db_NSE_V02.accdb",
):
    path = Path(file)
    if not path.is_file():
        msg = f"Invalid path\n{path}\nChange this path to your local MS Access db."
        raise ValueError(msg)
    return file


@pytest.fixture
def db_tables():
    # NOTE: Change this tuple of table mames to your local specs.
    the_tables = ("tbl_xprt_sales_grp", "tbl_xprt_part")
    return the_tables


def test_acc_engine(db_path):
    out = extr.get_engine(db_path)
    assert isinstance(out, engine.base.Engine)


def test_accs_err():
    with pytest.raises(FileNotFoundError):
        extr.get_engine(path="WRONG",
                        mode='Read',
                        driver= '{Microsoft Access Driver (*.mdb, *.accdb)}')
