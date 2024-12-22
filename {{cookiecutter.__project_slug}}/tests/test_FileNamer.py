import pytest
from src.s0_helpers import file_namer as fnr

from config import settings


@pytest.fixture
def data_paths():
    return settings.data_paths


def test_write_fn_default(name="base"):
    fnamer = fnr.FileNamer(name)
    out = fnamer.fname()
    target = "base.xlsx"
    assert out == target


def test_write_fn(name="base"):
    fnamer = fnr.FileNamer(name)
    out = fnamer.fname("lg", "z", ext=".tmp")
    # out = shunter.write_fn(name, "lg", "z", ext=".tmp")
    target = "base_lg_z.tmp"
    assert out == target


def test_write_fn_err(name=""):
    with pytest.raises(ValueError):
        fnr.FileNamer(name)