"""Test `final`"""

from src.s0_helpers.richtools import print_msg


def main(subproc: str | None = None) -> int:
    if subproc:
        msg = " ".join([__name__, subproc])
    else:
        msg = __name__
    print_msg(msg, type="info")
    return 0

if __name__ == "__main__":
    main()
