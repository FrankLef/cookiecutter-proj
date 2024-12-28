import pytest
import pandas as pd
from pathlib import Path
from src.s0_helpers import tdict as tdict_cls

from config import settings


@pytest.fixture
def tdict():
    a_path = Path(__file__).parents[1].joinpath("data")
    a_path = a_path.joinpath(settings.tdict)
    if not a_path.exists():
        msg = f"The TDict file was not found.\n{a_path}"
        raise FileNotFoundError(msg)
    data = pd.read_excel(a_path)
    obj = tdict_cls.TDict(data)
    return obj


def test_tdict(tdict):
    specs = tdict.get_data()
    assert not specs.empty


def test_tdict_err(tdict):
    with pytest.raises(UserWarning):
        tdict.get_data(role="wrong")
