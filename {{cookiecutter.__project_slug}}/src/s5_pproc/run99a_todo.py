"""A template to use within the `Preproc` directory."""

from rich import print as rprint


def main(is_skipped: bool =False) -> None:
    """Main function.

    Args:
        is_skipped (bool, optional): Skip this module if True. Defaults to False.

    Returns:
        int: Return an integer on the status.
    """
    if is_skipped:
        raise NotImplementedError(f"Skip the '{__name__}' script.")
    rprint(f"Executing the '{__name__}' script.")


if __name__ == "__main__":
    main()
