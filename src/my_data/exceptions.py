"""Module with `my-data` exceptions.

Contains exceptions for `my-data`.
"""


class MyDataException(Exception):
    """Base exception for My-Data-exceptions."""


class UnknownDatabaseTypeException(MyDataException):
    """Exception when a unknown database type is configured."""


class PermissionDeniedException(MyDataException):
    """Exception when a resource is created without the prober permissions."""


class WrongModelException(MyDataException):
    """Exception when a wrnog model is given."""
