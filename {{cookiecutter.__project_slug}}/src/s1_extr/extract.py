import logging
from time import gmtime, perf_counter, strftime

from rich.logging import RichHandler


logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
log = logging.getLogger("rich")


def main(subprocess) -> int:
    start = perf_counter()
    n = 0
    t = strftime("Elapsed time %H:%M:%S.", gmtime(perf_counter() - start))
    log.info("'%s' extracted %d files.\n%s", subprocess, n, t)
    return n
