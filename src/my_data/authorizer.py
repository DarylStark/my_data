"""APITokenAuthorizer class and Authorizers."""
from datetime import datetime
import logging
from abc import ABC, abstractmethod
from typing import Optional

from my_model import APIToken, User, UserRole

from my_data import MyData
from my_data.exceptions import UnknownUserAccountException

from .exceptions import (APITokenAuthorizerAlreadySetException,
                         AuthorizationFailed)


class APITokenAuthorizer:
    """Authorizer for API tokens.

    This Authorizer can be used to authorize users bases on a given API token.
    A specific Authorizer can be given to specify how authorization should be
    done.
    """

    def __init__(
            self,
            my_data_object: MyData,
            api_token: str | None = None,
            authorizer: 'Authorizer | None' = None):
        """Initialize the API token authorizer.

        Args:
            my_data_object: The MyData object to use.
            api_token: The API token to authorize with.
            authorizer: The authorizer to use.
        """
        self._logger = logging.getLogger(f'APITokenAuthorizer-{id(self)}')
        self._api_token_str = api_token
        self._authorizer: Optional[Authorizer] = None
        self.my_data_object = my_data_object

        # Set objects if authorizer is given
        if authorizer:
            self._authorizer = authorizer
            self._authorizer.set_api_token_authorizer(self)
            self._logger.debug('Authorizer "%s" is set', authorizer)

        # Caches
        self._user: Optional[User] = None
        self._api_token: Optional[APIToken] = None

    def _get_user(self) -> Optional[User]:
        """Get the user for the given API token.

        Returns:
            The user for the API token, or None if the API token is invalid.
        """
        if not self._api_token_str:
            return None

        my_data = self.my_data_object

        # Log in with a service user to retrieve the user.
        with my_data.get_context_for_service_user() as context:
            try:
                user = context.get_user_account_by_api_token(
                    api_token=self._api_token_str)
            except UnknownUserAccountException:
                pass
            else:
                return user
        return None

    def _get_api_token(self) -> Optional[APIToken]:
        """Get the API token for the given API token.

        Returns:
            The API token for the API token, or None if the API token is
            invalid.
        """
        if not self._api_token_str:
            return None

        my_data = self.my_data_object

        # Log in with a service user to retrieve the user.
        with my_data.get_context_for_service_user() as context:
            try:
                token = context.get_api_token_object_by_api_token(
                    api_token=self._api_token_str)
                # We have to load the scopes because they are laz loaded. We
                # don't save the scopes to somewhere else, because they are
                # already in the APIToken object.
                _ = token.token_scopes
            except UnknownUserAccountException:
                pass
            else:
                return token
        return None

    def _get_user_role(self) -> Optional[UserRole]:
        """Get the user role for the given API token.

        Returns:
            The user role for the API token, or None if the API token is
            invalid.
        """
        user = self.user
        if user:
            return user.role
        return None

    def authorize(self) -> None:
        """Authorize the user.

        This method is delegated to the authorizer. This way, the configured
        authorizer can be used to authorize the user and the user of the
        library can decide which authorize-scheme to use.
        """
        if self._authorizer:
            self._authorizer.authorize()

    @property
    def user(self) -> Optional[User]:
        """Get the user for the given API token.

        When the user is not loaded yet, it will be loaded from the database
        and cached. When the user is already loaded, the cached user will be
        returned.

        Returns:
            The user for the API token, or None if the API token is invalid.
        """
        if not self._user:
            self._user = self._get_user()
        return self._user

    @property
    def api_token(self) -> Optional[APIToken]:
        """Get the API token for the given API token.

        When the API token is not loaded yet, it will be loaded from the
        database and cached. When the API token is already loaded, the cached
        API token will be returned.

        Returns:
            The API token for the API token, or None if the API token is
            invalid.
        """
        if not self._api_token:
            self._api_token = self._get_api_token()
        return self._api_token

    @property
    def is_valid_user(self) -> bool:
        """Check if the user is a valid user.

        Returns:
            True if the user is a valid user, False otherwise.
        """
        return self.user is not None

    @property
    def is_root(self) -> bool:
        """Check if the user is a root user.

        Returns:
            True if the user is a root user, False otherwise.
        """
        return self._get_user_role() == UserRole.ROOT

    @property
    def is_normal_user(self) -> bool:
        """Check if the user is a normal user.

        Returns:
            True if the user is a normal user, False otherwise.
        """
        return self._get_user_role() == UserRole.USER

    @property
    def is_service_user(self) -> bool:
        """Check if the user is a service user.

        Returns:
            True if the user is a service user, False otherwise.
        """
        return self._get_user_role() == UserRole.SERVICE

    @property
    def is_long_lived_token(self) -> bool:
        """Check if the token is a long lived token.

        Returns:
            True if the token is a long lived token, False otherwise.
        """
        if not self.api_token:
            return False
        return self.api_token.api_client_id is not None

    @property
    def is_short_lived_token(self) -> bool:
        """Check if the token is a short lived token.

        Returns:
            True if the token is a short lived token, False otherwise.
        """
        if not self.api_token:
            return False
        return self.api_token.api_client_id is None

    @property
    def is_not_expired(self) -> bool:
        """Check if the token is not expired.

        Returns:
            False if the token is expired, True otherwise.
        """
        if self.api_token:
            return self.api_token.expires > datetime.utcnow()
        return False

    @property
    def is_enabled(self) -> bool:
        """Check if the token is enabled.

        Returns:
            True if the token is enabled, False otherwise.
        """
        if self.api_token:
            return self.api_token.enabled
        return False

    @property
    def is_valid_token(self) -> bool:
        """Check if the token is valid.

        Returns:
            True if the token is valid, False otherwise.
        """
        return (self.is_valid_user and
                self.is_not_expired and
                self.is_enabled)


class Authorizer(ABC):
    """Base class for authorizers."""

    def __init__(
            self,
            api_token_authorizer: Optional[APITokenAuthorizer] = None
    ) -> None:
        """Initialize the authorizer.

        Args:
            api_token_authorizer: the API token authorizer.
        """
        self._api_token_authorizer: Optional[APITokenAuthorizer] = \
            api_token_authorizer

    def set_api_token_authorizer(
            self,
            api_token_authorizer: APITokenAuthorizer) -> None:
        """Set the API token authorizer.

        Fails if the API token authorizer is already set.

        Args:
            api_token_authorizer: the API token authorizer.

        Raises:
            APITokenAuthorizerAlreadySetException: when the API token
                authorizer is already set.
        """
        if self._api_token_authorizer is not None:
            raise APITokenAuthorizerAlreadySetException(
                'API token authorizer is already set.')
        self._api_token_authorizer = api_token_authorizer

    @abstractmethod
    def authorize(self) -> None:
        """Authorize the user."""


class InvalidTokenAuthorizer(Authorizer):
    """Authorizer for logged off users.

    This authorizer will only fail if the user is logged on. If there
    is no user logged on, the authorization will succeed. This can be useful
    for endpoints that are only accessible for logged off users.
    """

    def authorize(self) -> None:
        """Authorize the user and fail if he is logged on.

        If the user is logged on, a exception will be raised.

        Raises:
            AuthorizationFailed: when the user it logged on.
        """
        if (self._api_token_authorizer and
                self._api_token_authorizer.is_valid_user):
            raise AuthorizationFailed


class ValidTokenAuthorizer(Authorizer):
    """Authorizer for logged on users.

    This authorizer will only fail if the user is not logged on. If there
    is a user logged on, the authorization will succeed. This can be useful
    for endpoints that are only accessible for logged on users, but that don't
    need any special permissions.
    """

    def authorize(self) -> None:
        """Authorize the user and fail if he is not logged on.

        If the user is not logged on, a exception will be raised.

        Raises:
            AuthorizationFailed: when the user it not logged on.
        """
        if (not self._api_token_authorizer or
                not self._api_token_authorizer.is_valid_token):
            raise AuthorizationFailed


class ShortLivedTokenAuthorizer(ValidTokenAuthorizer):
    """Authorization for logged on users with short lived tokens.

    This authorizer will fail if the logged on user is logged on with a API
    token that is not a short lived token. We subclass this class from
    LoggedOnAutorizer, because we want to reuse the authorize method.
    """

    def authorize(self) -> None:
        """Fails if he is not logged on with a short lived token.

        If the user is not logged on with a short lived token, a exception
        will be raised.

        Raises:
            AuthorizationFailed: when the user is not logged on with a
                short lived token.
        """
        super().authorize()
        if (not self._api_token_authorizer or
                not self._api_token_authorizer.is_short_lived_token):
            raise AuthorizationFailed


class APIScopeAuthorizer(ValidTokenAuthorizer):
    """Authorization for logged on users with API scope.

    This authorizer will fail if the given API scope is not given to the long
    lived token. It will always pass on short lived tokens, except when the
    argument 'allow_short_lived' is set to False.
    """

    def __init__(self,
                 required_scopes: list[str] | str,
                 allow_short_lived: bool = True) -> None:
        """Set the allowed scopes.

        Args:
            required_scopes: the required scopes. The API token has to be given
                all of these scopes to pass the authorization.
            allow_short_lived: specifies if short lived tokens are allowed. If
                this is set to False, short lived tokens will fail the
                authorization. Defaults to True.
        """
        super().__init__()
        self._required_scopes = required_scopes
        self._allow_short_lived = allow_short_lived

    def authorize(self) -> None:
        """Fails if the user is not logged on with the given API scope.

        If the user is not logged on with the given API scope, a exception
        will be raised.

        Raises:
            AuthorizationFailed: when the user is not logged on with the
                given API scope.
        """
        super().authorize()
        if self._api_token_authorizer:
            api_token = self._api_token_authorizer.api_token
            if api_token:
                if self._api_token_authorizer.is_long_lived_token:
                    scopes = [scope.full_scope_name
                              for scope in api_token.token_scopes]
                    for allowed_scope in self._required_scopes:
                        if allowed_scope not in scopes:
                            raise AuthorizationFailed
                    return
                if self._api_token_authorizer.is_short_lived_token:
                    if self._allow_short_lived:
                        return
        raise AuthorizationFailed
