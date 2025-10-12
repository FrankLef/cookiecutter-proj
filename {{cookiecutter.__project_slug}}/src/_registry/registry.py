"""Module used to hold constants and shared values."""

import os

def msg_hello() -> str:
    """Example function for the registry.

    Args:
        name (str, optional): Name to use to say hello. Defaults to "Ephel".

    Returns:
        str: Hello message.
    """
    msg = "[cyan]" + " ".join(["\u2139", "Hello", os.getlogin()]) + "[/cyan]"
    return msg