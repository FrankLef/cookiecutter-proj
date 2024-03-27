"""Connect to PostgreSQL database."""

from sqlalchemy import create_engine, URL
from sqlalchemy.engine.base import Engine  # for type hint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session  # for type hint (does not work, why?)
from sqlalchemy_utils import database_exists  # type:ignore
# from urllib.parse import quote_plus

# source: https://www.youtube.com/watch?v=neW9Y9xh4jc
# source: https://docs.sqlalchemy.org/en/20/orm/session_basics.html


specs: dict[str, str] = {
    "db": "tuba_skinny",
    "user": "postgres",
    "passwd": "p@ssword",
    "host": "localhost",
    "port": "5432",
    "driver": "postgresql+psycopg2",
}


def get_engine(
    db: str = specs["db"],
    user: str = specs["user"],
    passwd: str = specs["passwd"],
    host: str = specs["host"],
    port: str = specs["port"],
    driver: str = specs["driver"],
) -> Engine:
    """Create engine to access PostgreSQL database.

    Args:
        db (str, optional): Name of database. Defaults to specs['db'].
        user (str, optional): User name. Defaults to specs['user'].
        passwd (str, optional): Password. Defaults to specs['passwd'].
        host (str, optional): Name of host. Defaults to specs['host'].
        port (str, optional): Port address. Defaults to specs['port'].
        driver (str, optional): Name of driver. Defaults to specs['driver'].

    Raises:
        FileExistsError: PostgreSQL database was not found.

    Returns:
        Engine: Engine postgreSQL.
    """
    # NOTE: You must use parse.quote_plus from urllib to avoid problem with the password when it contains characters such as '@' which creates an invalid url.
    # passwd = quote_plus(passwd)
    # url = rf"{driver}://{user}:{passwd}@{host}:{port}/{db}"
    # NOTE: this is the best way!
    url = URL.create(
        drivername=driver,
        username=user,
        password=passwd,
        host=host,
        port=int(port),
        database=db,
    )
    if not database_exists(url):
        msg = f"Invalid database url\n{url}"
        raise FileExistsError(msg)
    engine = create_engine(url=url, pool_size=50, echo=False)
    return engine


def get_session() -> Session:
    """Create an sqlalchemy session for postgreSQL."""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    engine.dispose()
    return session


if __name__ == "__main__":
    session = get_session()
    print(session)
