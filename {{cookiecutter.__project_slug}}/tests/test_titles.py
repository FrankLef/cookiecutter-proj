"""Test the graphics classes."""

import pytest
from src.s0_helpers.graphics.titles import ITitles


class TestTitle(ITitles):

    def write_title(self, text: str | None = None):
        self.title = text

    def write_subtitle(self, text: str | None = None):
        self.subtitle = text


@pytest.fixture
def a_title():
    a_title = TestTitle(title="This is a title.", subtitle="This is a subtitle.")
    return a_title


def test_title(a_title):
    """Write a title."""
    text = "This is a test title."
    a_title.write_title(text)
    assert a_title.title == text


def test_subtitle(a_title):
    """Write a subtitle."""
    text = "This is a test subtitle."
    a_title.write_subtitle(text)
    assert a_title.subtitle == text


def test_main(a_title):
    text = a_title.write_main()
    target = "This is a title.<br>This is a subtitle."
    assert text == target


def test_html(a_title):
    """Write a text in html using the geom of the title object."""
    main_title = "The main title."
    text = a_title.write_html(text=main_title)
    target = "<span style='color: navy; font-size: 12px; font-family: DejaVu Sans'>The main title.</span>"
    assert text == target
