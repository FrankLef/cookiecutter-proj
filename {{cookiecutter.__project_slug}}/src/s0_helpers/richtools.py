from rich import print as rprint

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

# Define custom progress bar
# ssource: https://timothygebhard.de/posts/richer-progress-bars-for-rich/
progress_bar = Progress(
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    BarColumn(),
    MofNCompleteColumn(),
    TextColumn("•"),
    TimeElapsedColumn(),
    TextColumn("•"),
    TimeRemainingColumn(),
)


def create_msg(text: str, type: str | None = None) -> str:
    """Format a string to output to console using `rich`.

    Args:
        text (str): Text of the main body..
        type (str | None, optional): Format type. Defaults to None.

    Raises:
        ValueError: The type is invalid.

    Returns:
        str: Formatted string to use by `rich`.
    """
    if type is None:
        # if type is None, do nothing and return the text as is.
        return text
    else:
        a_type = type
        a_type = a_type.lower()

    match a_type:
        case "msg":
            fmt = ("[grey69]", " ", "[/grey69]")
        case "modul":
            # no space after symbol
            fmt = ("[purple]", "\u2022", "[/purple]")
        case "doc":
            fmt = ("[dim purple]", " ", "[/dim purple]")
        case "info":
            fmt = ("[cyan]", "\u2139 ", "[/cyan]")
        case "success":
            # no space after symbol
            fmt = ("[green]", "\u2713", "[/green]")
        case "warn":
            fmt = ("[yellow]", "\u26a0 ", "[/yellow]")
        case "fail":
            fmt = ("[red]", "\u2716 ", "[/red]")
        case "process":
            fmt = ("[gold1]", "\u2026", "[/gold1]")
        case _:
            raise ValueError(f"'{a_type}' is an invalid rich msg type.")

    if type != "process":
        msg = fmt[0] + " ".join([fmt[1], text]) + fmt[2]
    else:
        msg = fmt[0] + " ".join([text, fmt[1]]) + fmt[2]
    return msg


def print_msg(text: str, type: str|None = None) -> str:
    """Sent message to console using `rich`.

    Args:
        text (str): The text to print.
        type (str | None, optional): Format type. Defaults to None.

    Returns:
        str: Formatted string to use by `rich`.
    """
    msg = create_msg(text, type=type)
    rprint(msg)
    return msg


def print_modul(
    modul, modul_type: str = "modul", doc_type: str = "doc", verbose: bool = True
) -> str:
    """Print message for module. Usually with `importlib`."""
    msg = f"Module '{modul.__name__}' is imported"
    msg = create_msg(msg, type=modul_type)
    if verbose & (modul.__doc__ is not None):
        msg = msg + "\n" + create_msg(modul.__doc__, type=doc_type)
    rprint(msg)
    return msg
