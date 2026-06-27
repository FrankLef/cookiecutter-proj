"""Main CLI entry point."""

import typer
from pathlib import Path

from fltk.workflow import workflow as wf  # type: ignore

app = typer.Typer()

root_path = Path(__file__).parent
wf_path = root_path.joinpath("_workflow")
workflow = wf.WorkFlow(root=root_path, wf_path=wf_path)


@app.command()
def pipe(jobs: str, pat: str | None = None) -> None:
    """Run a pipe of commands.

    The `jobs` argument is a comma-separated string with the job's id. Job ids must be one of 'se', 'ex', 'tr', 'lo', 'ra', 'pp', 'ed', 'te'. For example, you can use 'ex,tr' for 'extract' then 'transform'. The order does not matter.
    The `jobs` is case-insensitive. All spaces are removed. The task id could be any word as long as it starts with the proper two letter. For example 'transform_it, EXT' is the same as 'ex,tr'.  If a task appears more that once, it will be processed only once.

    Args:
        jobs (str): comma-separated string with the jobs.
        pat (str | None, optional): Regex patttern passed on to the command to fitler files. Defaults to None.

    Returns:
        int: The sum of all the integers returned by the jobs.
    """
    workflow.execute(jobs_args=jobs, pat=pat)


@app.command()
def all(pat: str | None = None) -> None:
    """Run all modules except teardown.

    Args:
        pat (str | None, optional): Patttern passed on to the command to fitler files. Defaults to None.

    Returns:
        int: Integer returned by the process.
    """
    jobs = "se,ex,tr,lo,ra,pp,ed"
    workflow.execute(jobs_args=jobs, pat=pat)


if __name__ == "__main__":
    app()
