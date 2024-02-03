
import logging

from rich.logging import RichHandler

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
log = logging.getLogger("rich")

import etl.extract_url as extr  # noqa
import etl.sim as sim  # noqa

# import pyarrow.feather as feather  # noqa


def run_etl(size: int, seed: int, url: str):
    """Examples of data extraction.

    Args:
        size (int, optional): Sample size of a multivariate normal simulation.
        seed (int, optional): Seed of the multivariate normal sampling.
        url (str, optional): A url to test `requests`.

    Returns:
        dict: _description_
    """
    the_sim = sim.sim_df(size=size, seed=seed)
    log.debug("Sim has shape %s.", the_sim.shape)
    # the_sim.info()
    the_url_data = extr.extract_url(url)
    # the_url_data.info()
    return {"sim": the_sim, "url_data": the_url_data}


if __name__ == "__main__":
    size: int = 5
    seed: int = 1009
    a_url = r"https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv"  # noqa: E501
    run_etl(size=size, seed=seed, url=a_url)
