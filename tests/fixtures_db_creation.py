"""Module with DB creation fixtures.

TODO: documentation.
"""
from pytest import fixture
from my_data.my_data import MyData

# Import scheme
from my_model.global_models import APIScope, Field
from my_model.user_scoped_models import User


@fixture
def my_data() -> MyData:
    """TODO: documentation. """
    my_data = MyData()
    my_data.configure(
        db_connection_str='sqlite:////home/dast/my.sqlite',
        database_args={
            'echo': True,
            'pool_pre_ping': True,
            'pool_recycle': True,
            # 'pool_size': 5
        }
    )
    my_data.create_engine()
    my_data.create_db_tables()
    return my_data
