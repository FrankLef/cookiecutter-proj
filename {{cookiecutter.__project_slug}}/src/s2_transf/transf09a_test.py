"""Test `transf`"""

import warnings
import src.s0_helpers.richtools as rt


def main(is_skipped: bool = False) -> int:
    if is_skipped:
        msg = f"{__name__} is skipped."
        warnings.warn(msg, category=UserWarning)
        return 0
    rt.print_msg(__name__, type="info")
    return 0


if __name__ == "__main__":
    main()
