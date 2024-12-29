import pytest
import pandas as pd
import json
from pathlib import Path

# https://stackoverflow.com/questions/34466027/what-is-conftest-py-for-in-pytest


@pytest.fixture
def tdict_df():
    df = pd.read_json("tests/fixtures/tdict.json")
    return df

@pytest.fixture
def data_paths():
    with open("tests/fixtures/data_paths.json") as f:
        out = json.load(f)
    return out

@pytest.fixture
def data_path():
    a_path = Path(__file__).parents[1].joinpath("data")
    return a_path