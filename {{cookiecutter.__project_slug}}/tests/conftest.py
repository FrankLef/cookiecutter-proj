import pytest
import pandas as pd

# https://stackoverflow.com/questions/34466027/what-is-conftest-py-for-in-pytest

@pytest.fixture
def tdict_df():
    df = pd.read_json("tests/fixtures/tdict.json")
    return df