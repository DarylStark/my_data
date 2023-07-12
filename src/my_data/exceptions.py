"""Module with `my-data` exceptions.

Contains exceptions for `my-data`.
"""


class MyDataException(Exception):
    """Base exception for My-Data-exceptions."""


class DatabaseNotConfiguredException(MyDataException):
    """Raised when the database is not configured."""


class DatabaseConnectionException(MyDataException):
    """Error that happends when the database string is not correct."""
