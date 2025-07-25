"""TODO `raw`."""

import warnings
import src.s0_helpers.richtools as rt


def main(is_skipped: bool = False) -> int:
    """Main function.

    Args:
        is_skipped (bool, optional): Skip this module if True. Defaults to False.

    Returns:
        int: Return an integer on the status.
    """
    if is_skipped:
        warnings.warn(f"{__name__} is skipped.", category=UserWarning)
        return 0
    rt.print_msg(__name__, type="info")
    return 0


if __name__ == "__main__":
    main()
