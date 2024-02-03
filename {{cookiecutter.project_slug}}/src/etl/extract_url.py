import io
import logging

import pandas as pd
import requests
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
log = logging.getLogger("rich")


def extract_url(url: str) -> pd.DataFrame | None:
    assert len(url), "url is empty."
    resp = requests.get(url)
    resp.raise_for_status()
    # print(r.headers["content-type"])
    content = resp.content.decode("utf-8")
    df = pd.read_csv(io.StringIO(content))
    # df.info()
    return df
