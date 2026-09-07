"""Main CLI entry point."""

from pathlib import Path

import typer
from fltk.scriptrun.main import ScriptRun  # type: ignore

app = typer.Typer()

project_path = Path(__file__).parents[1]
process = ScriptRun(project_path, work_dirs=["src"], mode="importlib")


@app.command()
def pipe(jobs: str, pat: str | None = None, tim: bool = False) -> None:
    """Run a pipe of jobs (directories).

    Args:
        jobs (str): Comma-separated string with the job names.
        pat (str | None, optional): Regex pattern of file. Defaults to None.
        tim (bool, optional): Run with a timer if True. Defaults to False.
    """
    process.execute(job_args=jobs, file_pat=pat, with_timer=tim)


@app.command()
def all(pat: str | None = None, tim: bool = False) -> None:
    """Run all jobs except setup and teardown.

    Args:
        pat (str | None, optional): Regex pattern of file. Defaults to None.
        tim (bool, optional): Run with a timer if True. Defaults to False.
    """
    jobs = "etl, pproc, rollup, survey, outl, eda"
    process.execute(job_args=jobs, file_pat=pat, with_timer=tim)


if __name__ == "__main__":
    app()
