"""Methods for working with the SQLAlchemy ORM connected to the VPfG database."""

import logging
from typing import Union

import sqlalchemy
from sqlalchemy.orm import Session
from utilities.orm.models import Base

import warnings
from cryptography.utils import CryptographyDeprecationWarning

warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

logger = logging.getLogger(__name__)


def create_new_tables() -> None:
    """Creates new tables in database.

    Run after creating new models in utilities.orm.models

    This does not recreate tables that already exist. The simplest method to do that (assuming total data loss in the table is acceptable) is to run delete_table() followed by create_new_tables()
    """
    Base.metadata.create_all(get_engine())
    tables = Base.metadata.tables.keys()
    permission_query = ""
    for table in tables:
        permission_query += f'grant all on "{table}" to vpfg_prod;\n'
        permission_query += f'grant all on "{table}" to vpfg_dev;\n'
    query(permission_query, commit=True)


def get_session() -> Session:
    """SQLAlchemy session.

    Meant to be used as a context manager:
    ```
    # Add one row to candidate table
    with get_session() as session:
        candidate = Candidate(
            candidate_name = 'Jimmy John',
            state = 'CA',
            ...
        )
        session.add(candidate)
        session.commit()

    # Query all rows from candidate table
    with get_session() as session:
        all_candidates = session.query(Candidate).all()
    ```
    """
    engine = get_engine()
    session = sqlalchemy.orm.Session(engine)
    return session


def get_engine() -> sqlalchemy.engine.base.Engine:
    """Fetch a SQLAlchemy engine connected to the VPfG postgres database.

    Intended usage:
    ```
    with get_engine().connect() as connection:
        response = connection.execute('select * from some_table')
        result = response.fetchall()
    ```
    """
    pool = sqlalchemy.create_engine(
        "sqlite:///hackathon.db",
    )
    return pool


def load_rows_to_database(row_objects: Union[list[Base], Base]) -> None:
    """Loads new SQLAlchemy objects to database.

    ```
    user = User(email=email)
    load_rows_to_database(user)
    ```
    """
    if isinstance(row_objects, Base):
        row_objects = [row_objects]

    with get_session() as session:
        for row_object in row_objects:
            session.add(row_object)
        session.commit()

    logger.info(f"Loaded rows to database. [rows={len(row_objects)}]")


def query(
    sql: str, parameters: Union[list, dict, None] = None, commit: bool = False
) -> list[sqlalchemy.engine.row.Row] | None:
    """Execute SQL query directly against VPfG postgres database.

    Optionally specify parameters. Use %s to parameterize query.
    Example:
    ```
    names = ['John', 'Jimmy', 'James']
    result = query(
        "select * from names_table where name in %s",
        parameters=[tuple(names)]
    )
    result = query(
        "select * from names_table where name in %(names)s",
        parameters={'names': names}
    )
    ```
    """
    with get_engine().connect() as connection:
        response = connection.execute(sqlalchemy.text(sql), parameters=parameters)
        if commit:
            connection.commit()
    try:
        result = response.fetchall()
    except sqlalchemy.exc.ResourceClosedError:
        # Some queries, like create table statements, have no return
        result = None
    return result
