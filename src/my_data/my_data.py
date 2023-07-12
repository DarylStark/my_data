"""Module with the main class `MyData`.

This module contains the class `MyData`, which is the most important class for
the complete project.
"""

from typing import Any

from sqlalchemy.exc import OperationalError
from sqlalchemy.future import Engine
from sqlmodel import SQLModel, create_engine

from .exceptions import (DatabaseConnectionException,
                         DatabaseNotConfiguredException)


class MyData:
    """Main class for the library.

    This class creates the database connection and has a method to expose a
    context.

    Attributes:
        database_engine: the SQLmodel Engine.
        _database_str: the database connection string.
        _database_args: the arguments for the SQLalchemy connection.
    """

    def __init__(self) -> None:
        """Set default values.

        The initiator sets all values to `None`. We can later override these
        values with the `configure` method.
        """
        self.database_engine: Engine | None = None
        self._database_str: str | None = None
        self._database_args: dict[str, Any] | None = None

    def configure(self,
                  db_connection_str: str,
                  database_args: dict[str, Any] | None = None) -> None:
        """Set the database configuration.

        The database configuration is used when the database connection has to
        be made.

        Args:
            db_connection_str: the database connection string for the
                SQLmodel model.
            database_args: a dict with extra configuration for SQLmodel.
        """
        self._database_str = db_connection_str
        self._database_args = database_args

    def create_engine(self, force: bool = True) -> None:
        """Create the database connection.

        Creates the database connection with the given configuration. If the
        configuration is not set, it will raise an exception.

        Args:
            force: if set to True, the database connection will be created even
                if the database connection is already created.

        Raises:
            DatabaseNotConfiguredException: database not configured.
            DatabaseConnectionException: error while connecting to the
                database.
        """
        # Stop if there is already a database engine
        if self.database_engine is not None and not force:
            return

        # Check if the database connection is set
        if self._database_str is None:
            raise DatabaseNotConfiguredException(
                'Database is not configured yet')

        # Connect to the database
        database_args: dict[str, Any] = {
            'url': self._database_str
        }
        if self._database_args:
            database_args.update(self._database_args)

        # Create the database engine
        try:
            self.database_engine = create_engine(**database_args)
        except OperationalError as sa_error:
            raise DatabaseConnectionException(
                'Couldn\'t connect to database') from sa_error

    def create_db_tables(self, drop_tables: bool = False) -> None:
        """Create the defined models as tables.

        Method to create all tables that are defined in models.

        Args:
            drop_tables: determines if tables should be dropped prior to
                creating them. SQLalchemy will only drop the tables it
                knows about.
        """
        self.create_engine()

        if drop_tables:
            SQLModel.metadata.drop_all(self.database_engine)
        SQLModel.metadata.create_all(self.database_engine)
