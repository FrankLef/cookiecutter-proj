import pytest
from pathlib import Path
import src.s0_helpers.shunt_files as shunter

from config import settings

@pytest.fixture
def data_paths():
    return settings.data_paths

def test_write_fn_default(name="base"):
    out = shunter.write_fn(name)
    target = "base.xlsx"
    assert out == target

def test_write_fn(name="base"):
    out = shunter.write_fn(name, "lg", "z", ext=".tmp")
    target = "base_lg_z.tmp"
    assert out == target

def test_write_fn_err(name=""):
    with pytest.raises(AssertionError):
        shunter.write_fn(name)
        
def test_get_data_path(data_paths, id="raw"):
    a_path = shunter.get_data_path(id=id)
    print(a_path)
    a_dir = data_paths[id]
    target = Path(__file__).parents[1].joinpath("data", a_dir)
    assert a_path == target

def test_get_data_path_keyerr(id="wrong"):
    with pytest.raises(KeyError):
        shunter.get_data_path(id=id)
        
def test_get_data_path_direrr(id="raw"):
    with pytest.raises(NotADirectoryError):
        shunter.get_data_path(id=id, sub="wrong")
