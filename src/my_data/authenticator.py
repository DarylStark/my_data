"""Authenticator class and authenticators."""
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional

from my_model import APIToken, User, UserRole

from .my_data import MyData

from .exceptions import (AuthenticationFailed,
                         AuthenticatorNotConfiguredException,
                         UnknownUserAccountException,
                         UserAuthenticatorAlreadySetException)


class UserAuthenticator:
    """Authenticator for users."""

    def __init__(
            self,
            my_data_object: MyData,
            authenticator: 'Authenticator') -> None:
        """Initialize the user authenticator.

        Args:
            my_data_object: the MyData object to use.
            authenticator: the authenticator to use. This authenticator will
                be used to authenticate the user. This way, the authenticator
                can be changed at runtime.
        """
        self._logger = logging.getLogger(f'UserAuthenticator-{id(self)}')
        self._authenticator: Authenticator = authenticator
        self._authenticator.set_user_authenticator(self)
        self.my_data_object: 'MyData' = my_data_object

    def authenticate(self) -> User:
        """Authenticate the user.

        This method is delegated to the authenticator. This way, the configured
        authenticator can be changed at runtime.

        Returns:
            The authenticated user.
        """
        return self._authenticator.authenticate()

    def create_api_token(
            self,
            session_timeout_in_seconds: int,
            title: str) -> str:
        """Create a API token for the authenticated user.

        Creates a API token for the authenticated user and returns the created
        token.

        Args:
            session_timeout_in_seconds: the session timeout in seconds.
            title: The title of the API token.

        Returns:
            The created API token.
        """
        # Create token object with random token
        new_api_token = APIToken(
            api_client_id=None,
            title=title,
            expires=datetime.now() + timedelta(
                seconds=session_timeout_in_seconds))
        token = new_api_token.set_random_token()

        # Create token in database from the context of the user that is
        # authenticated. This way, we can be sure that the user has the
        # permission to create the token and that the token is created for the
        # correct user.
        user = self.authenticate()
        with self.my_data_object.get_context(user=user) as context:
            self._logger.debug('Creating API token for user %s',
                               user.username)
            context.api_tokens.create(new_api_token)
        return token


class Authenticator(ABC):
    """Abstract base class for authenticators."""

    def __init__(self,
                 user_authenticator: Optional[UserAuthenticator] = None):
        """Initialize the authenticator.

        Args:
            user_authenticator: The user authenticator to use.
        """
        self._user_authenticator = user_authenticator

    def set_user_authenticator(self, user_authenticator: UserAuthenticator):
        """Set the API authenticator.

        Args:
            user_authenticator: The user authenticator to use.

        Raises:
            UserAuthenticatorAlreadySetException: when the user authenticator
                is already set.
        """
        if self._user_authenticator is not None:
            raise UserAuthenticatorAlreadySetException(
                'Authenticator is already set.')
        self._user_authenticator = user_authenticator

    def _raise_for_invalid_authenticator(self) -> None:
        """Raise an exception when the authenticator is not configured.

        Raises:
            AuthenticatorNotConfiguredException: when the authenticator is not
                configured.
        """
        if not self._user_authenticator:
            raise AuthenticatorNotConfiguredException(
                'Authenticator is not configured.')

    @abstractmethod
    def authenticate(self) -> User:
        """Authenticate the user.

        Returns:
            The authenticated user.
        """


class CredentialsAuthenticator(Authenticator):
    """Authenticator for credentials.

    Authenticates a user using his username, saved (hashed) password and
    optionally a two-factor authentication code. Gives a error when this
    fails.
    """

    def __init__(
        self,
        username: str,
        password: str,
        second_factor: Optional[str],
        api_authenticator: Optional['UserAuthenticator'] = None
    ) -> None:
        """Initialize the credentials authenticator.

        Sets the given credentials by the user and optionally a second factor.
        The API authenticator can be set, but this is not required at this
        moment. It has to be set for the `authenticate` method.

        Args:
            username: The username to use.
            password: The password to use.
            second_factor: The second factor to use.
            api_authenticator: The API authenticator to use.
        """
        super().__init__(user_authenticator=api_authenticator)
        self._username = username
        self._password = password
        self._second_factor = second_factor

    def authenticate(self) -> User:
        """Authenticate the user.

        Will validate credentials and return the user if valid. If the user
        is a service user, the authentication will fail.

        Returns:
            The authenticated user.

        Raises:
            AuthenticationFailed: when the authentication fails.
        """
        self._raise_for_invalid_authenticator()
        my_data = self._user_authenticator.my_data_object  # type:ignore

        with my_data.get_context_for_service_user() as context:  # type: ignore
            try:
                user = context.get_user_account_by_username(
                    username=self._username)

                if (user.second_factor is None and
                        self._second_factor is not None):
                    raise UnknownUserAccountException

                valid_credentials = user.verify_credentials(
                    username=self._username,
                    password=self._password,
                    second_factor=self._second_factor)

                if (valid_credentials and
                        (user.role is not UserRole.SERVICE)):
                    return user
            except UnknownUserAccountException:
                pass

        raise AuthenticationFailed
