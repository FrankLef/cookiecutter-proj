import pytest
from src.s0_helpers import file_namer as fnamer_cls

from config import settings


@pytest.fixture
def data_paths():
    return settings.data_paths

@pytest.fixture
def fnamer():
    return fnamer_cls.FileNamer()


def test_write_fn_default(fnamer, name="base"):
    out = fnamer.fname(name)
    target = "base.xlsx"
    assert out == target


def test_write_fn(fnamer, name="base"):
    out = fnamer.fname(name, "lg", "z", ext=".tmp")
    # out = shunter.write_fn(name, "lg", "z", ext=".tmp")
    target = "base_lg_z.tmp"
    assert out == target


def test_write_fn_err(fnamer, name=""):
    with pytest.raises(ValueError):
        fnamer.fname(name)