import pytest
import src.s0_helpers.tdict as tdict


def test_tdict():
    df = tdict.main()
    assert not df.empty

def test_tdict_err():
    with pytest.raises(ValueError):
        tdict.main(role_rgx="wrong")
