"""Module with fixtures to create a test-database.

Fixture to create a test database for PyTest.
"""
# pylint: disable=redefined-outer-name

from pytest import fixture

from my_data import MyData
from my_data.authenticator import UserAuthenticator
from my_data.authorizer import APITokenAuthorizer


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
        }
    )

    # Create the engine and the test data
    my_data.create_engine()
    # TODO: Make this path not relative
    my_data.create_init_data('./tests/test_data.json')

    # Configure the Authenticator to use this database
    UserAuthenticator.configure(
        my_data_object=my_data,
        service_username='service.user',
        service_password='service_password'
    )

    # Configure the Authorizer to use this database
    APITokenAuthorizer.configure(
        my_data_object=my_data,
        service_username='service.user',
        service_password='service_password'
    )

    # Return the created object
    return my_data
