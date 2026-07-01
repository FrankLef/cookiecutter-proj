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
    "duckdb": project_path.joinpath("data", settings.duckdb),
    "data_setup": project_path.joinpath("data", settings.dpaths.setup),
    "data_extr": project_path.joinpath("data", settings.dpaths.extr),
    "data_transf": project_path.joinpath("data", settings.dpaths.transf),
    "data_load": project_path.joinpath("data", settings.dpaths.load),
    "data_raw": project_path.joinpath("data", settings.dpaths.raw),
    "data_pproc": project_path.joinpath("data", settings.dpaths.pproc),
    "data_eda": project_path.joinpath("data", settings.dpaths.eda),
    "data_teard": project_path.joinpath("data", settings.dpaths.teard),
    "reports": project_path.joinpath("reports"),
    "reports_data": project_path.joinpath("reports", "data"),
    "reports_figs": project_path.joinpath("reports", "figs"),
}
