"""Database class.

This module contains the main class: Database. As stated in the docstring for
the package, this can be used as a object with the database connection.
"""
from sqlalchemy.exc import OperationalError
from sqlalchemy.future import Engine
from sqlmodel import Session, SQLModel, create_engine

from .exceptions import DatabaseConnectionException


class Database:
    """Class for Database connection objects.

    Can be used to create a database connection and to retrieve Session objects
    from it.

    Attributes:
        connection_string: the connection string.
        echo: determines if queries should be echoed. This is usually only
            done for debugging purposes.
        pool_pre_ping: determines if the pool has to be checked prio to
            using it. This decreases performance, but increases
            reliability.
        pool_recycle: determines if used pools can be reused.
        pool_size: the amount of connections in the pool

        _engine: the SQLalchemy engine
    """

    def __init__(self) -> None:
        """Set default values.

        The initiator sets default values. These values are now set to defaults
        and should be overriden with the `configure` method. We do this so the
        user has the option to create the global object before specifing the
        details.
        """
        # Variables from the user. Should be set with `configure`
        self.connection_string: str = 'sqlite:///:memory'
        self.echo: bool = False
        self.pool_pre_ping: bool = True
        self.pool_recycle: int = 10
        self.pool_size: int = 5

        # Internal objects
        self._engine: Engine | None = None

    def configure(self,
                  connection_string: str) -> None:
        """Configure the database.

        The `configure` method configures the database connection. The user can
        use this method to set the connection string. The other configuration
        options should be set directly.

        Args:
            connection_string: the connection string.
        """
        # Variables from the user
        self.connection_string = connection_string

    def create_engine(self) -> None:
        """Create the SQLalchemy engine.

        Method to create the SQLalchemy engne. Can be done after setting the
        configuration details using the `configure` method.

        Raises:
            DatabaseConnectionException: when a connection couldn't be made.
        """
        try:
            # Create the engine
            self._engine = create_engine(
                url=self.connection_string,
                echo=self.echo,
                pool_pre_ping=self.pool_pre_ping,
                pool_recycle=self.pool_recycle,
                pool_size=self.pool_size
            )
        except OperationalError as sa_error:
            raise DatabaseConnectionException(
                'Couldn\'t connect to database') from sa_error

    def create_tables(self, drop_tables: bool = False) -> None:
        """Create the defined models as tables.

        Method to create all tables that are defined in models.

        Args:
            drop_tables: determines if tables should be dropped prior to
                creating them. SQLalchemy will only drop the tables it
                knows about.
        """
        if drop_tables:
            SQLModel.metadata.drop_all(self._engine)
        SQLModel.metadata.create_all(self._engine)

    def get_session(self, *args, **kwargs) -> Session:
        """Return a `Session` object.

        Method to get a Database Session.

        Args:
            *args: positional arguments for the Session
            **kwargs: named arguments for the Session

        Returns:
            The created Session object.
        """
        return Session(self._engine, *args, **kwargs)
