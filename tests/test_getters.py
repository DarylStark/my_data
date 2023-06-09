"""Tests for the getters of the ResourceModel.

Module that contains tests for the getters of the ResourceModel.
"""
from my_model.user import User

from database.database import Database
from my_data.context import Context


def test_get_users_normal(db: Database, normal_user: User) -> None:
    """Test to retrieve users as a normal user.

    Retrieves user in a normal user context. Should retrieve just one user; the
    current user. If more then this user is returned, or a different user, this
    unit test will fail.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        normal_user: the model for the normal user.
    """
    with Context(user=normal_user) as c:
        users = c.users.get()
        assert (users[0].username == 'daryl.stark')
        assert (len(users) == 1)


def test_get_users_root(db: Database, root_user: User) -> None:
    """Test to retrieve users as a root user.

    Retrieves user in a root user context. Should retrieve all users in the
    database.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        root_user: the model for the root user.
    """
    with Context(user=root_user) as c:
        users = c.users.get()
        assert (users[0].username == 'root')
        assert (users[1].username == 'daryl.stark')
        assert (len(users) == 2)


def test_tags(db: Database, normal_user: User) -> None:
    """Test to retrieve tags for a specific user.

    Should retrieve all tags that are created in the test database for the
    specific user.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        normal_user: the model for the normal user.
    """
    with Context(user=normal_user) as c:
        tags = c.tags.get()
        assert tags[0].title == 'test_daryl_1'
        assert tags[1].title == 'test_daryl_2'
