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

    Args:
        jobs (str): Comma-separated string with the jobs.
        pat (str | None, optional): Regex patttern to fitler files. Defaults to None.
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
    jobs = "etl,pproc,rollup,survey,outl,eda"
    workflow.execute(jobs_args=jobs, pat=pat)


@app.command()
def upload() -> None:
    """Upload data to MS Access."""
    workflow.execute(jobs_args="teard", pat="upload")

   
@app.command()
def compact() -> None:
    """Compact Duckdb."""
    workflow.execute(jobs_args="teard", pat="ddb_compact")


if __name__ == "__main__":
    app()
