"""Module with model fixtures.

Cotnains fixtures to mimick users. The `get_user_with_username` method is used
to get a specific user from the test database, as defined in the `MyData`
instance from the module `fixtures_db_creation`.
"""
from my_model.user_scoped_models import User, UserRole, Tag
from pytest import fixture
from sqlmodel import Session, select

from my_data.my_data import MyData


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


@fixture
def test_root_user() -> User:
    """Model for a ROOT user to create.

    Fixture for a user that can be used in the `creation` tests. This model is
    for a ROOT user.

    Returns:
        A model for a ROOT testuser.
    """
    return User(
        fullname='Creation Test Root User',
        username='creation_test_root_user_1',
        email='creation_test_root_user_1@example.com',
        role=UserRole.ROOT
    )


@fixture
def test_normal_user() -> User:
    """Model for a USER user to create.

    Fixture for a user that can be used in the `creation` tests. This model is
    for a USER user.

    Returns:
        A model for a USER testuser.
    """
    return User(
        fullname='Creation Test Normal User',
        username='creation_test_user_user_1',
        email='creation_test_user_user_1@example.com',
        role=UserRole.USER
    )


@fixture
def test_tags() -> list[Tag]:
    """Model for a tag to create.

    Fixture for a list of tags that can be used in the `creation` tests.

    Returns:
        A list with tags to create.
    """
    return [
        Tag(title='test_creation_tag_1'),
        Tag(title='test_creation_tag_2'),
        Tag(title='test_creation_tag_3')
    ]
