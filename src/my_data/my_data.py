"""Module with the main class `MyData`.

This module contains the class `MyData`, which is the most important class for
the complete project.
"""

import logging
from typing import Any

from my_model.user_scoped_models import User, UserRole
from sqlalchemy.exc import OperationalError
from sqlalchemy.future import Engine
from sqlmodel import Session, SQLModel, and_, create_engine, select

from .context import UserContext, ServiceContext
from .context_data import ContextData
from .exceptions import (DatabaseConnectionException,
                         DatabaseNotConfiguredException,
                         PermissionDeniedException)


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
        self._logger = logging.getLogger(f'MyData-{id(self)}')
        self._logger.info('MyData object created')
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
        self._logger.info('MyData object configured')

    def create_engine(self, force: bool = False) -> None:
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
            self._logger.debug('Database engine nog created beacause it ' +
                               'already exists and force is not set to True')
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
            self._logger.info('Database engine created')
        except OperationalError as sa_error:  # pragma: no cover
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

        if self.database_engine:
            if drop_tables:
                SQLModel.metadata.drop_all(self.database_engine)
            SQLModel.metadata.create_all(self.database_engine)
            self._logger.info('Database tables created')

    def get_context(self, user: User) -> UserContext:
        """Get a Context object for this database.

        Method to create a Context object and return it. The returned Context
        can be used in context manager right away, or as a `normal` object.

        Args:
            user: the user for the context. Is used in the ContextData object
                that is created for the Context object.

        Raises:
            DatabaseNotConfiguredException: method is called before configuring
                the database.

        Returns:
            The created Context object.
        """
        self.create_engine()

        # TODO: check if the given user is a normal user.

        if not self.database_engine:  # pragma: no cover
            raise DatabaseNotConfiguredException(
                'Database is not configured yet')

        return UserContext(
            database_engine=self.database_engine,
            context_data=ContextData(
                database_engine=self.database_engine,
                user=user)
        )

    def get_context_for_service_user(
            self, username: str, password: str) -> ServiceContext:
        """Get a Context object for the database as a service user.

        Method to create a Context object for a service user. The context can
        be used to do the things a service user needs to do, like retrieving
        user objects or API token objects.

        Args:
            username: the username for the service user.
            password: the password for the service user.

        Raises:
            DatabaseNotConfiguredException: method is called before configuring
                the database.
            PermissionDeniedException: when the credentials are incorrect.

        Returns:
            The created Context object.
        """
        self.create_engine()

        # TODO: check if the given user is a service user.

        if not self.database_engine:  # pragma: no cover
            raise DatabaseNotConfiguredException(
                'Database is not configured yet')

        with Session(self.database_engine) as session:
            sql_query = select(User)
            sql_query = sql_query.where(
                and_(User.username == username,
                     User.role == UserRole.SERVICE))
            users = session.exec(sql_query).all()

            # Check the amount of users we got
            if len(users) != 1:
                raise PermissionDeniedException(
                    f'Service account "{username}" does not exist')

            # Check if the provided credentials are correct
            user = users[0]
            if not user.verify_credentials(username, password):
                raise PermissionDeniedException(
                    f'Password for Service account "{username}" is incorrect')

            return ServiceContext(
                database_engine=self.database_engine,
                context_data=ContextData(
                    database_engine=self.database_engine,
                    user=user)
            )
