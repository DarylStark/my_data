"""Module with `my-data` exceptions.

Contains exceptions for `my-data`.
"""


class MyDataError(Exception):
    """Base exception for My-Data-exceptions."""


class DatabaseNotConfiguredError(MyDataError):
    """Raised when the database is not configured."""


class ServiceUserNotConfiguredError(MyDataError):
    """Raised when the service user is not configured."""


class DatabaseConnectionError(MyDataError):
    """Error that happends when the database string is not correct."""


class BaseClassCallError(MyDataError):
    """The Base class is used for a method that should be overriden."""


class WrongDataManipulatorError(MyDataError):
    """Wrong DataManipulator for specified model."""


class PermissionDeniedError(MyDataError):
    """User tries to do something he is not allowed to do."""


class UnknownUserAccountError(MyDataError):
    """Service user tries to retrieve a non-existing user account."""


class AthenticatorError(MyDataError):
    """Base exception for authenticator exceptions."""


class UserAuthenticatorAlreadySetError(AthenticatorError):
    """Raised when the API token authenticator is already set."""


class AuthenticatorNotConfiguredError(AthenticatorError):
    """Raised when the authenticator is not configured."""


class AuthenticationFailedError(AthenticatorError):
    """Raised when the authentication fails."""


class AuthorizerError(MyDataError):
    """Base exception for authorizer exceptions."""


class APITokenAuthorizerAlreadySetError(AuthorizerError):
    """Raised when the API token authorizer is already set."""


class AuthorizationFailedError(AuthorizerError):
    """Raised when the authorization fails."""
