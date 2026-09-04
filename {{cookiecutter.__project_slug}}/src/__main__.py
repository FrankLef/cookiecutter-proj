"""Main CLI entry point."""

import typer
from pathlib import Path

from fltk.scriptrun.main import ScriptRun  # type: ignore

app = typer.Typer()

project_path = Path(__file__).parents[1]
process = ScriptRun(project_path, work_dirs=["src"], mode="subprocess")


@app.command()
def pipe(jobs: str, pat: str | None = None) -> None:
    """Run a pipe of jobs (directories).

    The `jobs` argument is a comma-separated string with the jobs' names.

    Args:
        jobs (str): comma-separated string with the job names.
        pat (str | None, optional): Regex patttern passed on to the command to fitler files. Defaults to None.

    Returns:
        int: The sum of all the integers returned by the jobs.
    """
    process.execute(job_args=jobs, file_pat=pat)


@app.command()
def all(pat: str | None = None) -> None:
    """Run all modules except teardown.

    Args:
        pat (str | None, optional): Patttern passed on to the command to fitler files. Defaults to None.

    Returns:
        int: Integer returned by the process.
    """
    jobs = "setup, etl, pproc, rollup, survey, outl, eda"
    process.execute(job_args=jobs, file_pat=pat, with_timer=True)


if __name__ == "__main__":
    app()
