"""Exceptions for the Database package.

This module contains the exceptions that the Database package uses.
"""


class DatabaseException(Exception):
    """Base exception for Database-exceptions."""


class DatabaseConnectionException(DatabaseException):
    """Error that happends when the database string is not correct."""
