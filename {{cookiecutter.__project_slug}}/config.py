from pathlib import Path

from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.

project_path = Path(__file__).parent.absolute()
settings.paths = {
    "raw": project_path.joinpath("data", "raw"),
    "ready": project_path.joinpath("data", "ready"),
    "temp": project_path.joinpath("data", "temp"),
    "transf": project_path.joinpath("data", "transf"),
}
