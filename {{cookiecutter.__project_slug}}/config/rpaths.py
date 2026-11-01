from pathlib import Path
from typing import NamedTuple


def get_rpaths() -> NamedTuple:
    project_path = Path(__file__).parents[1]
    reports_path = project_path.joinpath("reports")

    class DataPaths(NamedTuple):
        reports: Path = reports_path
        data: Path = reports_path.joinpath("data")
        figs: Path = reports_path.joinpath("figs")

    return DataPaths()


RPATHS = get_rpaths()
