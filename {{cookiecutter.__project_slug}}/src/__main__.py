"""Main CLI entry point."""

import typer

from .run_moduls import main as run_cmd

app = typer.Typer()


@app.command()
def pipe(jobs: str, pat: str | None = None) -> int:
    """Run a pipe of commands.

    The `jobs` argument is a comma-separated string with the job's id. Job ids must be one of 'ex', 'tr', 'lo', 'ra', 'pp', 'ed', 'fi'. For example, you can use 'ex,tr' for 'extract' then 'transform'. The order does not matter.
    The `jobs` is case-insensitive. All spaces are removed. The task id could be any word as long as it starts with the proper two letter. For example 'transform_it, EXT' is the same as 'ex,tr'.  If a task appears more that once, it will be processed only once.

    Args:
        jobs (str): comma-separated string with the jobs.
        pat (str | None, optional): Regex patttern passed on to the command to fitler files. Defaults to None.

    Returns:
        int: The sum of all the integers returned by the jobs.
    """
    n = run_cmd(jobs=jobs, pat=pat)
    return n


@app.command()
def all(pat: str | None = None) -> int:
    """Run all modules.

    Args:
        pat (str | None, optional): Patttern passed on to the command to fitler files. Defaults to None.

    Returns:
        int: Integer returned by the process.
    """
    jobs = "ex,tr,lo,ra,pp,ed,fi"
    n = run_cmd(jobs=jobs, pat=pat)
    return n


if __name__ == "__main__":
    app()
