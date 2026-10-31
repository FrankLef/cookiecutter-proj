from dynaconf import Dynaconf
from pathlib import Path

config_dir = Path(__file__).parent.joinpath("config")

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[
        config_dir.joinpath("settings.toml"),
        config_dir.joinpath("specs.py"),
        config_dir.joinpath("dpaths.py"),
        config_dir.joinpath("rpaths.py"),
        config_dir.joinpath("ddb.py"),
        config_dir.joinpath("acc.py"),
    ],
    merge_enabled=True,
)
