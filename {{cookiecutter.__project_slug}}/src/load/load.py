"""Load data to MS Accesss."""

import logging
import sys
from pathlib import Path
from time import gmtime, perf_counter, strftime

from rich.logging import RichHandler

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
log = logging.getLogger("rich")

src_path = Path(__file__).parents[1]
if src_path not in sys.path:
    sys.path.insert(1, str(src_path))

project_path = src_path.parents[2]
if project_path not in sys.path:
    sys.path.insert(1, str(project_path))

# from config import settings  # noqa
# from .load_acc import load_acc as load  # noqa


# db_path = settings.paths.acc_db


def main(subprocess):
    start = perf_counter()
    # n = load_acc(subprocess)
    n = 0
    t = strftime("Elapsed time %H:%M:%S.", gmtime(perf_counter() - start))
    log.info("'%s' transformed %d files.\n%s", subprocess, n, t)
    return n
