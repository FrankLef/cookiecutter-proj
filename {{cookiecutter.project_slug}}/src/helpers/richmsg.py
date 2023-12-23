from rich import print


def create_msg(text: str, type: str = "info") -> str:
    """Create a string to output to console using `rich`.

    Args:
        text (str): Text of the main body.
        type (str, optional): Format id of the output. Defaults to "info".

    Returns:
        str: String in a format understood by `rich`.
    """
    type = type.lower()
    specs = {
        "info": ("[cyan]", "\u2139", "[/cyan]"),
        "success": ("[green]", "\u2713", "[/green]"),
        "warn": ("[yellow]", "\u0021", "[/yellow]"),
        "fail": ("[red]", "\u2716", "[/red]"),
        "process": ("[gold1]", "\u2026", "[/gold1]")
    }
    vals = specs[type]
    if type != "process":
        msg = vals[0] + " ".join([vals[1], text]) + vals[2]
    else:
        msg = vals[0] + " ".join([text, vals[1]]) + vals[2]
    return msg


def print_msg(text: str, type: str = "info") -> str:
    """Sent message to console using `rich`.

    Args:
        text (str): _description_
        type (str, optional): _description_. Defaults to "info".

    Returns:
        str: Message sent to the console.
    """
    msg = create_msg(text, type=type)
    print(msg)
    return msg
