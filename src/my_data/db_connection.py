"""Module with the `db_connection`.

This module contains the `db_connection` object. This object is created using
the `Database` class from the `database` package. This object is defined in a
seperate module so the complete package can use it. The application that is
using this library can configure this Database object using the factory methods
defined in the `database.factories` module.
"""
from database.database import Database

db_connection = Database()
