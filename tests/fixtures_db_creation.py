"""Module with fixtures to create a test-database.

Fixture to create a test database for PyTest.
"""
from pytest import fixture
from my_data import MyData


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
    my_data.create_init_data()

    # Return the created object
    return my_data
