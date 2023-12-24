import pytest
import sqlalchemy as sa

import src.etl.extract_acc as extr
from config import settings


@pytest.fixture
def db_path():
    return settings.msaccess.path


@pytest.fixture
def db_tables():
    return settings.msaccess.tables


def test_acc_engine(db_path):
    out = extr.build_engine(db_path)
    assert isinstance(out, sa.engine.base.Engine)


def test_accs_err():
    with pytest.raises(FileNotFoundError):
        extr.build_engine("wrong path")
