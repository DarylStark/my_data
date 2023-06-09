"""Module that contains function to configure the `my-data` library.

This module contains methods to create a database connection. This should be
used to configure the `my-data` package.
"""
from enum import Enum

from pydantic import BaseModel, validate_arguments

from database.database import Database
from database.factories import create_memory_sqlite_database

from .db_connection import db_connection
from .exceptions import UnknownDatabaseTypeException


class DatabaseType(Enum):
    """The possible Database Types.

    Attributes:
        SQLITE_MEMORY: a in-memory SQLite database.
        MYSQL: a MySQL database connection.
    """

    SQLITE_MEMORY = 1
    MYSQL = 1


class MyDataConfig(BaseModel):
    """Pydantic model to create objects for the `my-data` configuration.

    Model that contains the configuration parameters for `my-data`. This model
    can be used for the `configure` function to set the configuration.

    Attributes:
        db_type: the database type.
        db_username: the username for the database (if it is a database that
            requires a username).
        db_password: the password for the database (if it is a database that
            requires a password).
        db_database: the database-name.
        db_server: the server where the database lives.
        db_filename: the filename for the database.
    """

    db_type: DatabaseType
    db_username: str | None = None
    db_password: str | None = None
    db_database: str | None = None
    db_server: str | None = None
    db_filename: str | None = None


@validate_arguments
def configure(configuration: MyDataConfig) -> Database:
    """Configure the `my-data` package.

    Configure the `my-data` package by setting the configuration parameters.
    Takes in a MyDataConfig instance with the configuration data.

    Args:
        configuration: the configuration for the package.

    Returns:
        Database: the created Database object.

    Raises:
        UnknownDatabaseTypeException: a unknown database type is used.
    """
    if configuration.db_type == DatabaseType.SQLITE_MEMORY:
        return create_memory_sqlite_database(db_connection)

    # No correct database selected, give an error
    raise UnknownDatabaseTypeException(
        f'Database type {configuration.db_type} is not recognized.')
