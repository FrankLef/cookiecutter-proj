from pathlib import Path

import pytest

from config import settings


@pytest.fixture
def db_path():
    return settings.msaccess.path


@pytest.fixture
def db_tables():
    return tuple(settings.msaccess.tables)


def test_db_path(db_path):
    target = "C:/Users/Public/MyJob/DesjCap_cies/PHT/db_PHT_V1_xprt.accdb"
    assert db_path == target
    assert Path(db_path).exists()


def test_db_tables(db_tables):
    assert db_tables == ("tbl_xprt_sales_grp", "tbl_xprt_part")
