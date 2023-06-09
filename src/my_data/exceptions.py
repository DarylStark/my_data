"""Module with `my-data` exceptions.

Contains exceptions for `my-data`.
"""


class MyDataException(Exception):
    """Base exception for My-Data-exceptions."""


class UnknownDatabaseTypeException(MyDataException):
    """Exception when a unknown database type is configured."""
