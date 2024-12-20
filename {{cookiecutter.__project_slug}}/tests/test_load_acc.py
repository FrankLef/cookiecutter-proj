"""Test the MS Access connection."""

import pytest
from pathlib import Path
from sqlalchemy import engine

import src.s3_load.load_acc as extr


@pytest.fixture
def db_path(
    file: str = r"C:\Users\Public\MyAcctg\xbrl\db_xbr.accdb",
):
    path = Path(file)
    if not path.is_file():
        msg = f"Invalid path\n{path}\nChange this path to your local MS Access db."
        raise ValueError(msg)
    return path


@pytest.fixture
def db_tables():
    # NOTE: Change this tuple of table mames to your local specs.
    the_tables = ("qryx_xbr_concepts", "qryx_xbr_fstypes")
    return the_tables


def test_acc_engine(db_path):
    out = extr.build_engine(db_path)
    assert isinstance(out, engine.base.Engine)


def test_accs_err():
    fn = r"C:\Users\Public\MyAcctg\xbrl\wrong.accdb"
    a_path = Path(fn)
    with pytest.raises(FileNotFoundError):
        extr.build_engine(path=a_path)
