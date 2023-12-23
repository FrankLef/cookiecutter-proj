# from ruamel.yaml import YAML
import sys
from pathlib import Path

import extract_url as extr
import sim as sim
from prefect import flow

# import pyarrow.feather as feather  # noqa

# src path to be able to import the settings
src_path = Path(__file__).parent.parent

# add the project path to be able to access the settings
a_path = str(src_path.parent)
if a_path not in sys.path:
    sys.path.insert(1, a_path)

from config import settings  # noqa
from helpers import richmsg  # noqa

process_msg = settings.message.etl
a_url = settings.url


@flow(name="ETL", log_prints=True)
def run_etl(size: int = 5, seed: int = 1009, url: str = "") -> dict:
    """Extract, transform and load data.

    Args:
        size (int, optional): _description_. Defaults to 5.
        seed (int, optional): _description_. Defaults to 1009.
        url (str, optional): _description_. Defaults to "".

    Returns:
        dict: _description_
    """
    richmsg.print_msg(text=process_msg, type="process")
    if not url:
        url = a_url
    df1 = sim.sim_df(size=size, seed=seed)
    df1.info()
    df2 = extr.extract_url(url)
    df2.info()
    return {"sim": df1, "extract": df2}


if __name__ == "__main__":
    run_etl()
