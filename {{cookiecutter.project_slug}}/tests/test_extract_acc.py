"""Test the MS Access connections."""
import pytest
from pathlib import Path
import sqlalchemy as sa

import src.etl.extract_acc as extr


@pytest.fixture
def db_path():
    # NOTE: Change this path to your local MS Access db
    path = Path("C:/Users/Public/MyJob/DesjCap_cies/PHT/db_PHT_V1_xprt.accdb")
    return path


@pytest.fixture
def db_tables():
    # NOTE: Change this tuple of table mames to your local specs.
    the_tables = ("tbl_xprt_sales_grp", "tbl_xprt_part")
    return the_tables


def test_acc_engine(db_path):
    out = extr.build_engine(db_path)
    assert isinstance(out, sa.engine.base.Engine)


def test_accs_err():
    with pytest.raises(FileNotFoundError):
        extr.build_engine("wrong path")
