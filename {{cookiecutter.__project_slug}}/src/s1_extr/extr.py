import logging
from time import gmtime, perf_counter, strftime

from rich.logging import RichHandler

from .extr_test import main as extr_test

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
log = logging.getLogger("rich")


def main(subprocess: str) -> int:
    start = perf_counter()
    if subprocess != "test":
        n = 0
    elif subprocess == "test":
        n = extr_test(subprocess)
    else:
        msg = f"{subprocess} is an invalid subprocess."
        raise ValueError(msg)
    t = strftime("Elapsed time %H:%M:%S.", gmtime(perf_counter() - start))
    log.info("'%s' extracted %d files.\n%s", subprocess, n, t)
    return n
