"""Database factories.

Module that contains the factories to configure Database objects. The factories
can be used to easily create specific, predefined Database objects without the
need to remember, or look-up, the specific configuration parameters.
"""

from .database import Database


def create_memory_sqlite_database(
        database_object: Database | None) -> Database:
    """Create a in-memory SQLite Database-object.

    Factory function to create a in-memory SQLite database. Databases like this
    can be used for testing, for example. When the application finishes, the
    database is removed from RAM.

    Args:
        database_object: the database object that you want to modify. This is a
            optional argument. If you don't specify it, a new object will be
            created.

    Returns:
        Database: the created, or modified, Database object
    """
    # Create the object if none is set
    if database_object is None:
        database_object = Database()

    # Configure the database with the correct string. For a in-memory SQLite
    # database, taht should be `sqlite:///:memory:`
    database_object.configure('sqlite:///:memory:')
    database_object.create_engine()

    return database_object


def create_mysql_database(
        server: str,
        username: str,
        password: str,
        database: str,
        database_object: Database | None) -> Database:
    """Create a MySQL Database object.

    Factory function to create a Database object for a MySQL connection. This
    can be used for production workloaes.

    Args:
        server: the server address for the MySQL server
        username: the username to use when connecting
        password: the password to use when connecting
        database: the database to select
        database_object: the database object that you want to modify. This is a
            optional argument. If you don't specify it, a new object will be
            created.

    Returns:
        Database: the created, or modified, Database object
    """
    # Create the object if none is set
    if database_object is None:
        database_object = Database()

    # Configure the database with the correct string.
    database_object.configure(
        f'mysql+pymysql://{username}:{password}@{server}/{database}')
    database_object.create_engine()

    return database_object
