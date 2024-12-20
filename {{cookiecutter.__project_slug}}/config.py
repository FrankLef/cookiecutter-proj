from pathlib import Path

from dynaconf import Dynaconf  # type: ignore

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.

project_path = Path(__file__).parent.absolute()
settings.paths = {
    "data": project_path.joinpath("data"), 
    "temp": project_path.joinpath("data", "d0-temp"),
    "raw": project_path.joinpath("data", "d1-raw"),
    "transf": project_path.joinpath("data", "d2-transf"),
    "ready": project_path.joinpath("data", "d3-ready"),
    "preproc": project_path.joinpath("data", "d4-preproc"),
    "eda": project_path.joinpath("data", "d5-eda"),
    "final": project_path.joinpath("data", "d6-final"),
}
