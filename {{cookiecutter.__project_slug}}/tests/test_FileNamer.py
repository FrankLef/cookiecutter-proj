import pytest
from src.s0_helpers import file_namer as fnamer_cls


@pytest.fixture
def fnamer():
    return fnamer_cls.FileNamer()


def test_write_fn_default(fnamer, name="base"):
    out = fnamer.get_name(name)
    target = "base.xlsx"
    assert out == target


def test_write_fn(fnamer, name="base"):
    out = fnamer.get_name(name, "lg", "z")
    target = "base_lg_z.xlsx"
    assert out == target


def test_write_fn_err(fnamer, name=""):
    with pytest.raises(ValueError):
        fnamer.get_name(name)
