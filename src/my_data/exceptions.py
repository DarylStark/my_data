"""Module with `my-data` exceptions.

Contains exceptions for `my-data`.
"""


class MyDataException(Exception):
    """Base exception for My-Data-exceptions."""


class DatabaseNotConfiguredException(MyDataException):
    """Raised when the database is not configured."""


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
