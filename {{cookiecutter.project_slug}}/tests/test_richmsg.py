"""Test the richmsg.py module."""
import pytest

import src.helpers.richmsg as richmsg


def test_cli_info():
    text = "This is an information"
    target = "[cyan]" + " ".join(["\u2139", text]) + "[/cyan]"
    out = richmsg.create_msg(text=text, type="info")
    assert out == target


def test_cli_process():
    text = "Processing something"
    target = "[gold1]" + " ".join([text, "\u2026"]) + "[/gold1]"
    out = richmsg.create_msg(text=text, type="process")
    assert out == target


def test_cli_err():
    with pytest.raises(KeyError):
        text = "This is an information"
        richmsg.create_msg(text=text, type="WRONG")
