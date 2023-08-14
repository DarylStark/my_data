"""Module for the Context class.

This module contains the Context class.
"""
from types import TracebackType

from my_model.user_scoped_models import (APIClient, APIToken,  # type: ignore
                                         Tag, User, UserRole, UserSetting)
from sqlalchemy.future import Engine
from sqlmodel import select

from .context_data import ContextData
from .creators import UserCreator, UserScopedCreator
from .deleters import UserDeleter, UserScopedDeleter
from .exceptions import PermissionDeniedException, UnknownUserAccountException
from .resource_manager import ResourceManager
from .retrievers import UserRetriever, UserScopedRetriever
from .updaters import UserScopedUpdater, UserUpdater


class Context:
    """Context to work in.

    The Context class is used to create objects to interact with the database
    in a context-based way. A Context uses a ContextData object, which contains
    the data for the context (like a User to work with). The Context makes sure
    that every manipulation of the database is done with the permissions of the
    Context.

    Attributes:
        database_engine: the SQLalchemy engine to use.
        _context_data: specifies in what context to use Context.
    """

    def __init__(self,
                 database_engine: Engine,
                 context_data: ContextData) -> None:
        """Set the default values and create the needed DataManipulators.

        The initializer set the values and creates the needed DataManipulator
        objects. These objects are the objects that are used to manipulate the
        data in the database, like users and tags.

        Args:
            database_engine: a database engine to work with.
            context_data: the context data for this context.
        """
        self.database_engine = database_engine
        self._context_data = context_data

        # Exposure of Resource Managers to manage specific resources in the
        # data model.
        self.users = ResourceManager(
            database_model=User,
            database_engine=database_engine,
            context_data=self._context_data,
            creator=UserCreator,
            retriever=UserRetriever,
            updater=UserUpdater,
            deleter=UserDeleter)
        self.tags = ResourceManager(
            database_model=Tag,
            database_engine=database_engine,
            context_data=self._context_data,
            creator=UserScopedCreator,
            retriever=UserScopedRetriever,
            updater=UserScopedUpdater,
            deleter=UserScopedDeleter)
        self.api_clients = ResourceManager(
            database_model=APIClient,
            database_engine=database_engine,
            context_data=self._context_data,
            creator=UserScopedCreator,
            retriever=UserScopedRetriever,
            updater=UserScopedUpdater,
            deleter=UserScopedDeleter)
        self.api_tokens = ResourceManager(
            database_model=APIToken,
            database_engine=database_engine,
            context_data=self._context_data,
            creator=UserScopedCreator,
            retriever=UserScopedRetriever,
            updater=UserScopedUpdater,
            deleter=UserScopedDeleter)
        self.user_settings = ResourceManager(
            database_model=UserSetting,
            database_engine=database_engine,
            context_data=self._context_data,
            creator=UserScopedCreator,
            retriever=UserScopedRetriever,
            updater=UserScopedUpdater,
            deleter=UserScopedDeleter)

    def __enter__(self) -> 'Context':
        """Start a Python context manager.

        The start of a Context Manager. Should be used with the Python `with`
        statement.

        Returns:
            This own class.
        """
        return self

    def __exit__(self,
                 exception_type: BaseException | None,
                 exception_value: BaseException | None,
                 traceback: TracebackType | None) -> bool:
        """Exit of a Python context manager.

        The end of the context manager. Checks if there are any unhandled
        execeptions and returns True if there aren't.

        Args:
            exception_type: the type of exception that happened.
            exception_value: the value for the exception.
            traceback: a traceback for the exception.

        Returns:
            False if there are unhandled exceptions, True if there are none.
        """
        self._context_data.close_session()
        return exception_type is None

    def get_user_account_by_username(self, username: str) -> User:
        """Get a User account using a service account.

        Retrieves a User account for a user by searching for a specific
        username. This can only be done by a service user.

        Args:
            username: the username for the user.

        Raises:
            PermissionDeniedException: user in the context is not a Service
                user.
            UnknownUserAccountException: the user is not found.

        Returns:
            A User object for the correct user.
        """
        if self._context_data.user.role != UserRole.SERVICE:
            raise PermissionDeniedException('Should be ran as a service user')

        sql_query = select(User).where(User.username == username)
        if self._context_data.db_session:
            user_object = self._context_data.db_session.exec(sql_query).all()
        if len(user_object) == 1:
            return user_object[0]
        raise UnknownUserAccountException(
            f'User with username "{username}" is not found.')

    def get_user_account_by_api_token(self, api_token: str) -> User:
        """Get a User account using via a API token.

        Retrieves a User account for a user by searching for a specific API
        token. This can only be done by a service user.

        Args:
            api_token: the API token for the user.

        Raises:
            PermissionDeniedException: user in the context is not a Service
                user.
            UnknownUserAccountException: the user is not found.

        Returns:
            A User object for the correct user.
        """
        if self._context_data.user.role != UserRole.SERVICE:
            raise PermissionDeniedException('Should be ran as a service user')

        sql_query = select(APIToken).where(APIToken.token == api_token)
        api_tokens = self._context_data.db_session.exec(sql_query).all()
        if len(api_tokens) == 1:
            return api_tokens[0].user
        raise UnknownUserAccountException(
            f'Token "{api_token}" is not found.')
