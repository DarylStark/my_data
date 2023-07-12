"""Module with DB creation fixtures.

TODO: documentation.
"""
from pytest import fixture
from my_data.my_data import MyData

from sqlmodel import Session

# Import scheme
from my_model.global_models import APIScope
from my_model.user_scoped_models import User, UserRole, Tag


@fixture
def my_data() -> MyData:
    """TODO: documentation. """
    # Configure the database
    my_data = MyData()
    my_data.configure(
        # db_connection_str='sqlite:///:memory:',
        db_connection_str='sqlite:////home/dast/my.sqlite',
        database_args={
            'echo': True,
            'pool_pre_ping': True,
            'pool_recycle': True,
        }
    )

    # Create the engine and the test data
    my_data.create_engine()
    my_data.create_init_data()

    # Return the created object
    return my_data
