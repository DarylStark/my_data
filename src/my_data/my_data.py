"""Module with the main class `MyData`.

This module contains the class `MyData`, which is the most important class for
the complete project.
"""

import logging
from typing import Any, Optional

from sqlalchemy.exc import OperationalError
from sqlalchemy.future import Engine
from sqlmodel import Session, and_, create_engine, select

from my_model import User, UserRole

from .context import ServiceContext, UserContext
from .context_data import ContextData
from .exceptions import (DatabaseConnectionException,
                         DatabaseNotConfiguredException,
                         PermissionDeniedException,
                         ServiceUserNotConfiguredException)


class MyData:
    """Base class for the MyData objects.

    This class creates the database engine and keeps the connection alive. It
    serves as the base class for other classes that need to interact with the
    database.

    Attributes:
        database_engine: the SQLmodel Engine.
        _database_str: the database connection string.
        _database_args: the arguments for the SQLalchemy connection.
        _service_username: the username of the service user.
        _service_password: the password of the service user.
        _service_user_account: the User object for the service user. This is
            lazy loaded, so it is only loaded when it is needed.
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
        self._service_username: str | None = None
        self._service_password: str | None = None
        self._service_user_account: Optional[User] = None

    def configure(self,
                  db_connection_str: str,
                  database_args: dict[str, Any] | None = None,
                  service_username: str | None = None,
                  service_password: str | None = None) -> None:
        """Set the database configuration.

        The database configuration is used when the database connection has to
        be made.

        Args:
            db_connection_str: the database connection string for the
                SQLmodel model.
            database_args: a dict with extra configuration for SQLmodel.
            service_username: the username of a service user to use.
            service_password: the password of a service user to use.
        """
        self._database_str = db_connection_str
        self._database_args = database_args
        self._service_username = service_username
        self._service_password = service_password

        # Logging
        self._logger.info('MyData object configured')

    def _validate_service_user(self,) -> User:
        """Validate the service user.

        Method to check if the service user is configured. If not, it will
        raise an exception.

        Raises:
            ServiceUserNotConfiguredException: when the service user is not
                configured yet.
            PermissionDeniedException: when the credentials are incorrect.

        Returns:
            The User object for the Service User.
        """
        self.create_engine()

        if not self._service_username or not self._service_password:
            raise ServiceUserNotConfiguredException(
                'Service user is not configured yet')

        if not self._service_user_account:
            with Session(self.database_engine) as session:
                sql_query = select(User)
                sql_query = sql_query.where(
                    and_(User.username == self._service_username,
                         User.role == UserRole.SERVICE))
                users = session.exec(sql_query).all()

            # Check the amount of users we got
            if len(users) != 1:
                raise PermissionDeniedException(
                    f'Service account "{self._service_username}" does ' +
                    'not exist')

            # Check if the provided credentials are correct
            user = users[0]
            if not user.verify_credentials(
                    username=self._service_username,
                    password=self._service_password):
                raise PermissionDeniedException(
                    'Password for Service account ' +
                    f'"{self._service_username}" is incorrect')

            self._logger.info('Service user "%s" vaild',
                              self._service_username)
            self._service_user_account = user

        return self._service_user_account

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

    def get_context(self, user: User) -> UserContext:
        """Get a Context object for this database.

        Method to create a Context object and return it. The returned Context
        can be used in context manager right away, or as a `normal` object.

        Args:
            user: the user for the context. Is used in the ContextData object
                that is created for the Context object.

        Raises:
            PermissionDeniedException: method is called with a user that does
                not have the correct role.
            DatabaseNotConfiguredException: method is called before configuring
                the database.

        Returns:
            The created Context object.
        """
        self.create_engine()

        if user.role not in (UserRole.USER, UserRole.ROOT):
            raise PermissionDeniedException(
                'User does not have the correct role')

        if not self.database_engine:  # pragma: no cover
            raise DatabaseNotConfiguredException(
                'Database is not configured yet')

        return UserContext(
            database_engine=self.database_engine,
            context_data=ContextData(
                database_engine=self.database_engine,
                user=user)
        )

    def get_context_for_service_user(self) -> ServiceContext:
        """Get a Context object for the database as a service user.

        Method to create a Context object for a service user. The context can
        be used to do the things a service user needs to do, like retrieving
        user objects or API token objects.

        Raises:
            DatabaseNotConfiguredException: method is called before configuring
                the database.

        Returns:
            The created Context object.
        """
        self.create_engine()
        if not self.database_engine:
            raise DatabaseNotConfiguredException(  # pragma: no cover
                'Database is not configured yet')

        service_user = self._validate_service_user()

        return ServiceContext(
            database_engine=self.database_engine,
            context_data=ContextData(
                database_engine=self.database_engine,
                user=service_user)
        )
