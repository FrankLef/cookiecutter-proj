import pytest
import pandas as pd
import json
from pathlib import Path

# https://stackoverflow.com/questions/34466027/what-is-conftest-py-for-in-pytest


@pytest.fixture
def data_paths():
    with open("tests/fixtures/data_paths.json") as f:
        out = json.load(f)
    return out


@pytest.fixture
def data_path():
    a_path = Path(__file__).parents[1].joinpath("data")
    return a_path


@pytest.fixture
def dic1() -> pd.DataFrame:
    df = pd.read_json("tests/fixtures/dic1.json")
    return df


@pytest.fixture
def df1():
    df = pd.read_json("tests/fixtures/df1.json")
    return df


@pytest.fixture
def df1a():
    df = pd.read_json("tests/fixtures/df1a.json")
    return df


@pytest.fixture
def df2():
    df = pd.read_json("tests/fixtures/df2.json")
    return df
