import io

import pandas as pd
import requests as rq
from prefect import task

# Adelie penguins
# this takes about 7 min
a_url = r"https://doi.org/10.6073/pasta/98b16d7d563f265cb52372c8ca99e60f"
# Gentoo penguins
# this takes about 7 min
a_url = r"https://doi.org/10.6073/pasta/7fca67fb28d56ee2ffa3d9370ebda689"
# Chinstrap penguins
# this takes about 7 min
a_url = r"https://doi.org/10.6073/pasta/c14dfcfada8ea13a17536e73eb6fbe9e"
# NOTE: To find url of dataset in github, click on raw, then you will see the
# raw file.
# Then take the address in the url bar on top of the screen
a_url = r"https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv"  # noqa: E501


# r = rq.get(a_url)
#  if all is good rais_for_status will be None
# this is the favorite way to do it since it returns an exception in case of
# problem
# r.raise_for_status()
# print(r.headers["content-type"])
# to look at the header dictionnary
# print(r.headers.keys)
# d = pd.read_csv(io.StringIO(r.content.decode("utf-8")))
# d.info()


@task
def extract_url(url: str) -> pd.DataFrame | None:
    assert len(url), "url is empty."
    resp = rq.get(url)
    resp.raise_for_status()
    # print(r.headers["content-type"])
    content = resp.content.decode("utf-8")
    df = pd.read_csv(io.StringIO(content))
    # df.info()
    return df
