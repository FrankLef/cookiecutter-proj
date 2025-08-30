"""Test he existence of the table and data dictionaries."""

import src.s0_helpers.richtools as rt

from src.inst_tdic import main as tdic
from src.inst_ddic import main as ddic


def main() -> int:
    """This serves as a test to validate if the dics instantiate properly."""
    for name in ("main",):
        a_tdic = tdic(name)
        n = len(a_tdic.lines)
        msg = f"The '{name}' tdic instantiated with {n} lines."
        rt.print_msg(msg, type="info")
    for name in ("main", "xbr"):
        a_ddic = ddic(name)
        n = len(a_ddic.lines)
        msg = f"The '{name}' ddic instantiated with {n} lines."
        rt.print_msg(msg, type="info")
    return 1
