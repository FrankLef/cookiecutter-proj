"""Main CLI entry point."""

import typer
from pathlib import Path

# from fltk.jobrun.main import JobRun
from fltk.jobflow.main import JobFlow

app = typer.Typer()

project_path = Path(__file__).parents[1]
# process = JobRun(project_path, work_dirs=["src"])
process = JobFlow(project_path, work_dirs=["src"])


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
    process.execute(job_args=jobs, file_pat=None)


if __name__ == "__main__":
    app()
