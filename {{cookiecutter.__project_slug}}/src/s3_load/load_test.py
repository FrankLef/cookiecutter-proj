from src.s0_helpers.richtools import print_msg


def main(subproc: str) -> int:
    print_msg(" ".join([__name__, subproc]), type="msg")
    return 0
