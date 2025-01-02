import pytest

from src.s0_helpers import tdict as tdict_cls


@pytest.fixture
def tdict(tdict_df):
    obj = tdict_cls.TDict(tdict_df)
    return obj


def test_tdict(tdict):
    specs = tdict.get_data()
    assert specs.shape == (3, 13)

def test_tdict_activ(tdict):
    specs = tdict.get_data(activ=True)
    assert specs.shape == (2, 13)

def test_tdict_activ_err(tdict):
    with pytest.raises(AssertionError):
        tdict.get_data(activ='wrong')