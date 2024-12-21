import logging
from time import gmtime, perf_counter, strftime

from rich.logging import RichHandler

# from .transf_xl import main as transf_xl

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
log = logging.getLogger("rich")


def main(subprocess: str) -> int:
    start = perf_counter()
    n = 0
    t = strftime("Elapsed time %H:%M:%S.", gmtime(perf_counter() - start))
    log.info("'%s' transformed %d files.\n%s", subprocess, n, t)
    return n
