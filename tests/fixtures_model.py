"""Module with model fixtures.

Cotnains fixtures to mimick users. The `get_user_with_username` method is used
to get a specific user from the test database, as defined in the `MyData`
instance from the module `fixtures_db_creation`.
"""
from pytest import fixture
from my_data.my_data import MyData

from my_model.user_scoped_models import User

from sqlmodel import Session, select


def get_user_with_username(my_data: MyData, username: str) -> User | None:
    """Get a user with a specific username.

    Returns the user with a specific username from the databas.

    Args:
        my_data: a instance to a MyData object.
        username: the username to search for.

    Returns:
        The user object for the requested username
    """
    with Session(my_data.database_engine) as session:
        user = select(User).where(User.username == username)
        query = session.exec(user)
        return query.first()


@fixture
def root_user(my_data: MyData) -> User | None:
    """Root user.

    Fixture for a user with a ROOT role.

    Args:
        my_data: a instance to a MyData object.

    Returns:
        The User object or None if it isn't found.
    """
    return get_user_with_username(my_data, 'root')


@fixture
def normal_user_1(my_data: MyData) -> User | None:
    """The first normal user.

    Fixture for a user with a USER role.

    Args:
        my_data: a instance to a MyData object.

    Returns:
        The User object or None if it isn't found.
    """
    return get_user_with_username(my_data, 'normal.user.1')


@fixture
def normal_user_2(my_data: MyData) -> User | None:
    """The second normal user.

    Fixture for a user with a USER role.

    Args:
        my_data: a instance to a MyData object.

    Returns:
        The User object or None if it isn't found.
    """
    return get_user_with_username(my_data, 'normal.user.2')
