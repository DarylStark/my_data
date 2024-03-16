"""Module with fixtures to create a test-database.

Fixture to create a test database for PyTest.
"""
# pylint: disable=redefined-outer-name

import os

from my_data import MyData
from my_data.data_loader import DataLoader, JSONDataSource
from my_data.my_data_table_creator import MyDataTableCreator
from pydantic_settings import BaseSettings
from pytest import fixture


class ConfigurationForTests(BaseSettings):
    """Settings for testing."""

    db_string: str = 'sqlite:///:memory:'
    database_args: dict[str, str | bool | int] = {'echo': True}
    service_username: str = 'service.user'
    service_password: str = 'service_password'
    create_tables: bool = True
    import_data: bool = True


def test_filename() -> str:
    """Return the filename of the test data file.

    Returns:
        The filename of the test data file.
    """
    return os.path.join(os.path.dirname(__file__), 'test_data.json')


@fixture(scope='module')
def my_data() -> MyData:
    """Create a test database.

    Creates a testdatabase and returns the `MyData` object for it.

    Returns:
        The created `MyData` instance.
    """
    configuration = ConfigurationForTests()

    # Configure the database
    my_data = MyData()
    my_data.configure(
        db_connection_str=configuration.db_string,
        database_args=configuration.database_args,
        service_username=configuration.service_username,
        service_password=configuration.service_password,
    )

    # Create the engine
    my_data.create_engine()

    # Create the tables
    if configuration.create_tables:
        my_data_table_creator = MyDataTableCreator(my_data_object=my_data)
        my_data_table_creator.create_db_tables(drop_tables=True)

    # Create testdata
    if configuration.import_data:
        loader = DataLoader(
            my_data_object=my_data, data_source=JSONDataSource(test_filename())
        )
        loader.load()

    # Return the created object
    return my_data
