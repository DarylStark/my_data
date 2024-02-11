"""Module with fixtures to create a test-database.

Fixture to create a test database for PyTest.
"""
# pylint: disable=redefined-outer-name

import os

from pytest import fixture

from my_data import MyData
from my_data.data_loader import DataLoader, JSONDataSource


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
    # Configure the database
    my_data = MyData()
    my_data.configure(
        db_connection_str='sqlite:///:memory:',
        database_args={
            'echo': True
        },
        service_username='service.user',
        service_password='service_password'
    )

    # Create the engine and the tables
    my_data.create_engine()
    my_data.create_db_tables(drop_tables=True)

    # Create testdata
    loader = DataLoader(
        my_data_object=my_data,
        data_source=JSONDataSource(
            test_filename()))
    loader.load()

    # Return the created object
    return my_data
