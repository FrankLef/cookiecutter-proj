"""Configuration settings used by dynaconf"""
from dynaconf import Dynaconf  # type: ignore
from pathlib import Path

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.

project_path = Path(__file__).parent.absolute()
settings.paths = {
    "data": project_path.joinpath("data"),
    "data_temp": project_path.joinpath("data", "d0_temp"),
    "data_extr": project_path.joinpath("data", "d1_extr"),
    "data_transf": project_path.joinpath("data", "d2_transf"),
    "data_load": project_path.joinpath("data", "d3_load"),
    "data_raw": project_path.joinpath("data", "d4_raw"),
    "data_pproc": project_path.joinpath("data", "d5_pproc"),
    "data_eda": project_path.joinpath("data", "d6_eda"),
    "data_final": project_path.joinpath("data", "d7_final"),
}