"""Module with `my-data` exceptions.

Contains exceptions for `my-data`.
"""


class MyDataException(Exception):
    """Base exception for My-Data-exceptions."""


class DatabaseNotConfiguredException(MyDataException):
    """Raised when the database is not configured."""


class ServiceUserNotConfiguredException(MyDataException):
    """Raised when the service user is not configured."""


class DatabaseConnectionException(MyDataException):
    """Error that happends when the database string is not correct."""


class BaseClassCallException(MyDataException):
    """The Base class is used for a method that should be overriden."""


class WrongDataManipulatorException(MyDataException):
    """Wrong DataManipulator for specified model."""


class PermissionDeniedException(MyDataException):
    """User tries to do something he is not allowed to do."""


class UnknownUserAccountException(MyDataException):
    """Service user tries to retrieve a non-existing user account."""


class AthenticatorExceptions(MyDataException):
    """Base exception for authenticator exceptions."""


class UserAuthenticatorAlreadySetException(AthenticatorExceptions):
    """Raised when the API token authenticator is already set."""


class AuthenticatorNotConfiguredException(AthenticatorExceptions):
    """Raised when the authenticator is not configured."""


class AuthenticationFailed(AthenticatorExceptions):
    """Raised when the authentication fails."""


class AuthorizerExceptions(MyDataException):
    """Base exception for authorizer exceptions."""


class APITokenAuthorizerAlreadySetException(AuthorizerExceptions):
    """Raised when the API token authorizer is already set."""


class AuthorizationFailed(AuthorizerExceptions):
    """Raised when the authorization fails."""
