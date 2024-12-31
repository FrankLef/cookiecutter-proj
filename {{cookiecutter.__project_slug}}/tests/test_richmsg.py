"""Test the richmsg.py module."""

import src.s0_helpers.richtools as richtools


def test_cli_info():
    text = "This is an information"
    target = "[cyan]" + " ".join(["\u2139 ", text]) + "[/cyan]"
    out = richtools.create_msg(text=text, type="info")
    assert out == target


def test_cli_process():
    text = "Processing something"
    target = "[gold1]" + " ".join(["\u2022", text]) + "[/gold1]"
    out = richtools.create_msg(text=text, type="process")
    assert out == target