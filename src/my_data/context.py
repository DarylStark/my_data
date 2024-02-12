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

from sqlalchemy.future import Engine
from sqlalchemy.sql.elements import ColumnElement
from sqlmodel import select

from my_model import APIClient, APIScope, APIToken, Tag, User, UserSetting

from .context_data import ContextData
from .exceptions import UnknownUserAccountException
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

        The initializer sets the values for the database engine and the context
        data. If a subclass of Context is created, the subclass should call
        this initializer and add additional attributes to the subclass.

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
        self.commit_session()
        self.close_session()
        return exception_type is None

    def commit_session(self) -> None:
        """Commit the database session.

        Method to commit the changes in the session. This should be done when
        the Context is ready with this ContextData object. This is either done
        in the closure of the Python Context Manager, or when the user chooses
        to close it.
        """
        self._context_data.commit_session()

    def close_session(self) -> None:
        """Close the database session.

        Method to close the session. This should be done when the Context is
        ready with this ContextData object. This is either done in the closure
        of the Python Context Manager, or when the user chooses to close it.
        """
        self._context_data.close_session()

    def abort_session(self) -> None:
        """Abort the database session.

        Method to abort the changes in the session. This is not done
        automatically and should be invoked by the user when he made changes
        that should be aborted before commited. After the abort, the session
        is _not_ closed; the user has to do that himself.
        """
        self._context_data.abort_session()


class UserContext(Context):
    """Context for normal users.

    This context exposes the Resource Managers to manage specific resources in
    the data model.
    """

    def __init__(self,
                 database_engine: Engine,
                 context_data: ContextData) -> None:
        """Init the UserContext.

        The initializer set the values and creates the needed DataManipulator
        objects. These objects are the objects that are used to manipulate the
        data in the database, like users and tags.

        Args:
            database_engine: a database engine to work with.
            context_data: the context data for this context.
        """
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
        super().__enter__()
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

        Returns:
            A User object for the correct user.
        """
        self._logger.debug('Retrieving API token object by API token')
        return self.get_api_token_object_by_api_token(api_token).user

    def get_api_scopes(self,
                       module: str | None = None,
                       subject: str | None = None) -> list[APIScope]:
        """Get the API scopes from the database.

        Retrieves the API scopes from the database. Can be filtered with
        the `title` and `subject` arguments.

        Args:
            module: filter on the module.
            subject: filter on the subject.

        Returns:
            A list of retrieved APIScope objects.
        """
        self._logger.debug('Retrieving all API scopes')

        flt: list[ColumnElement[bool]] = []
        if module:
            flt.append(APIScope.module == module)  # type: ignore
        if subject:
            flt.append(APIScope.subject == subject)  # type: ignore

        # Create the query
        sql_query = select(APIScope)

        # Add the filters
        for filter_item in flt:
            sql_query = sql_query.where(filter_item)

        # Execute the query
        api_scopes: list[APIScope] = []
        if self._context_data.db_session:
            api_scopes = list(
                self._context_data.db_session.exec(sql_query).all())

        # Return the items
        return api_scopes

    def __enter__(self) -> 'ServiceContext':
        """Start a Python context manager for a ServiceContext.

        The start of a Context Manager. Should be used with the Python `with`
        statement.

        Returns:
            This own class.
        """
        super().__enter__()
        return self
