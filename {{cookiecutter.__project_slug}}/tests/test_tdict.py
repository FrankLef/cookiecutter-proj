import pytest
from pathlib import Path
from src.s0_helpers import tdict as tdict_cls

from config import settings

@pytest.fixture
def tdict_path():
    a_path = Path(__file__).parents[1].joinpath("data")
    a_path = a_path.joinpath(settings.tdict)
    return a_path


def test_tdict(tdict_path):
    tdict = tdict_cls.TDict(tdict_path)
    specs = tdict.get_specs()
    assert not specs.empty


def test_tdict_err(tdict_path):
    tdict = tdict_cls.TDict(tdict_path)
    with pytest.raises(ValueError):
        tdict.get_specs(role_rgx="wrong")
