import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
log = logging.getLogger("rich")


def main(text: str, n: int) -> bool:
    log.info("Dispatching \'%s\' with n = %d.", text, n)
    return True
