"""TODO: documentation.
"""
from pytest import fixture
from my_data import MyData


@fixture
def my_data() -> MyData:
    """TODO: documentation. """
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
