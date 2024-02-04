"""Module for the Context classes.

This module contains the Context classes for the application. There are two
types of context classes; one for normal users (root and normal users) and one
for service users. The Context classes are used to create objects to interact
with the database in a context-based way. A Context uses a ContextData object,
which contains the data for the context (like a User to work with). The Context
makes sure that every manipulation of the database is done with the permissions
of the Context.s
"""
import logging
from types import TracebackType

from my_model.user_scoped_models import (APIClient, APIToken, Tag, User,
                                         UserRole, UserSetting)
from sqlalchemy.future import Engine
from sqlmodel import select

from .context_data import ContextData
from .exceptions import PermissionDeniedException, UnknownUserAccountException
from .resource_manager import (UserResourceManagerFactory,
                               UserScopedResourceManagerFactory)


class Context:
    """Context to work in.

    The Context class is used to create objects to interact with the database
    in a context-based way. A Context uses a ContextData object, which contains
    the data for the context (like a User to work with). The Context makes sure
    that every manipulation of the database is done with the permissions of the
    Context.

    This class is the baseclass for Contexts. We can create different type of
    Contexts using this baseclass. For example, we can create a Context for
    normal users and a Context for service users.

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
        self._logger = logging.getLogger(f'Context-{id(self)}')
        self.database_engine = database_engine
        self._context_data = context_data

    def __enter__(self) -> 'Context':
        """Start a Python context manager.

        The start of a Context Manager. Should be used with the Python `with`
        statement.

        Returns:
            This own class.
        """
        self._logger.debug('Context object as context manager started')
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
        self._logger.debug('Context object as context manager closed')
        self._context_data.close_session()
        return exception_type is None


class UserContext(Context):
    """Context for normal users.

    This context exposes the Resource Managers to manage specific resources in
    the data model.
    """

    def __init__(self,
                 database_engine: Engine,
                 context_data: ContextData) -> None:
        super().__init__(database_engine, context_data)

        # Exposure of Resource Managers to manage specific resources in the
        # data model.
        self.users = UserResourceManagerFactory(
            database_model=User,
            database_engine=database_engine,
            context_data=self._context_data).create()
        self.tags = UserScopedResourceManagerFactory(
            database_model=Tag,
            database_engine=database_engine,
            context_data=self._context_data).create()
        self.api_clients = UserScopedResourceManagerFactory(
            database_model=APIClient,
            database_engine=database_engine,
            context_data=self._context_data).create()
        self.api_tokens = UserScopedResourceManagerFactory(
            database_model=APIToken,
            database_engine=database_engine,
            context_data=self._context_data).create()
        self.user_settings = UserScopedResourceManagerFactory(
            database_model=UserSetting,
            database_engine=database_engine,
            context_data=self._context_data).create()

    def __enter__(self) -> 'UserContext':
        """Start a Python context manager for a UserContext.

        The start of a Context Manager. Should be used with the Python `with`
        statement.

        Returns:
            This own class.
        """
        self.__enter__()
        return self


class ServiceContext(UserContext):
    """Context for service users.

    This context exposes the methods that only Service users can use.
    """

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
        self._logger.debug('Retrieving user account by username: %s', username)

        sql_query = select(User).where(User.username == username)
        if self._context_data.db_session:
            user_object = self._context_data.db_session.exec(sql_query).all()
            if len(user_object) == 1:
                self._logger.debug('User account: "%d"', user_object[0].id)
                return user_object[0]
        raise UnknownUserAccountException(
            f'User with username "{username}" is not found.')

    def get_api_token_object_by_api_token(self, api_token: str) -> APIToken:
        """Get a User account using via a API token.

        Retrieves a APIToken object for a user by searching for a specific API
        token. This can only be done by a service user.

        Args:
            api_token: the API token for the user.

        Raises:
            PermissionDeniedException: user in the context is not a Service
                user.
            UnknownUserAccountException: the user is not found.

        Returns:
            A APIToken object for the API token.
        """
        self._logger.debug('Retrieving API token object by API token')

        sql_query = select(APIToken).where(APIToken.token == api_token)
        api_tokens = self._context_data.db_session.exec(sql_query).all()
        if len(api_tokens) == 1:
            self._logger.debug('API token object: "%d"', api_tokens[0].id)
            return api_tokens[0]
        raise UnknownUserAccountException(
            f'Token "{api_token}" is not found.')

    def get_user_account_by_api_token(self, api_token: str) -> User:
        """Get a User account using via a API token.

        Retrieves a User account for a user by searching for a specific API
        token. This can only be done by a service user.

        Args:
            api_token: the API token for the user.

        Raises:
            PermissionDeniedException: user in the context is not a Service
                user.

        Returns:
            A User object for the correct user.
        """
        self._logger.debug('Retrieving API token object by API token')
        return self.get_api_token_object_by_api_token(api_token).user

    def __enter__(self) -> 'ServiceContext':
        """Start a Python context manager for a ServiceContext.

        The start of a Context Manager. Should be used with the Python `with`
        statement.

        Returns:
            This own class.
        """
        self.__enter__()
        return self
