from pathlib import Path
from typing import NamedTuple


def get_dpaths() -> NamedTuple:
    project_path = Path(__file__).parents[1]
    data_path = project_path.joinpath("data")

    class DataPaths(NamedTuple):
        data: Path = data_path
        setup: Path = data_path.joinpath("d0_setup")
        extr: Path = data_path.joinpath("d1_extr")
        transf: Path = data_path.joinpath("d2_transf")
        load: Path = data_path.joinpath("d3_load")
        pproc: Path = data_path.joinpath("d4_pproc")
        rollup: Path = data_path.joinpath("d5_rollup")
        survey: Path = data_path.joinpath("d6_survey")
        outl: Path = data_path.joinpath("d7_outl")
        eda: Path = data_path.joinpath("d8_eda")
        teard: Path = data_path.joinpath("d9_teard")

    return DataPaths()


DPATHS = get_dpaths()
