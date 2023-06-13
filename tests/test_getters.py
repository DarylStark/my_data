"""Tests for the getters of the ResourceManager.

Module that contains tests for the getters of the ResourceManager.
"""
from my_model.user import User
from pytest import raises

from database.database import Database
from my_data.context import Context
from my_data.db_models import DBTag, DBUser
from my_data.exceptions import InvalidFilterFieldException


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


def test_users_raw_filters(db: Database, root_user: User) -> None:
    """Test to retrieve users as root with a raw filter.

    Should retrieve users the context based on specific raw filters.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        root_user: the model for the root user.
    """
    with Context(user=root_user) as c:
        # Test specific match
        users = c.users.get(raw_filters=[DBUser.username == 'root'])
        assert users[0].username == 'root'
        assert len(users) == 1

        # Test specific unmatch
        users = c.users.get(raw_filters=[DBUser.username != 'root'])
        assert users[0].username == 'daryl.stark'
        assert len(users) == 1

        # Test bigger then
        users = c.users.get(raw_filters=[DBUser.id > 0])
        assert users[0].username == 'root'
        assert users[1].username == 'daryl.stark'
        assert len(users) == 2

        # Test smaller then
        users = c.users.get(raw_filters=[DBUser.id < 99])
        assert users[0].username == 'root'
        assert users[1].username == 'daryl.stark'
        assert len(users) == 2


def test_users_named_filters(db: Database, root_user: User) -> None:
    """Test to retrieve tags for a specific user with named filters.

    Should retrieve users for the the context based on specific named filters.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        root_user: the model for the root user.
    """
    with Context(user=root_user) as c:
        # Test specific match
        users = c.users.get(username='daryl.stark')
        assert users[0].username == 'daryl.stark'
        assert len(users) == 1

        # Test if something that is invalid is not found indeed
        users = c.users.get(username='emilia.clarke')
        assert len(users) == 0

        # Test if a invalid field results in a exception
        with raises(InvalidFilterFieldException):
            users = c.users.get(unknown_field='test')


def test_tags_raw_filters(db: Database, normal_user: User) -> None:
    """Test to retrieve tags for a specific user with a raw filter.

    Should retrieve tags for the user in the context based on specific raw
    filters.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        normal_user: the model for the normal user.
    """
    with Context(user=normal_user) as c:
        # Test specific match
        tags = c.tags.get(raw_filters=[DBTag.title == 'test_daryl_2'])
        assert tags[0].title == 'test_daryl_2'
        assert len(tags) == 1

        # Test specific unmatch
        tags = c.tags.get(raw_filters=[DBTag.title != 'test_daryl_2'])
        assert tags[0].title == 'test_daryl_1'
        assert len(tags) == 1

        # Test bigger then
        tags = c.tags.get(raw_filters=[DBTag.id > 0])
        assert tags[0].title == 'test_daryl_1'
        assert tags[1].title == 'test_daryl_2'
        assert len(tags) == 2

        # Test smaller then
        tags = c.tags.get(raw_filters=[DBTag.id < 999])
        assert tags[0].title == 'test_daryl_1'
        assert tags[1].title == 'test_daryl_2'
        assert len(tags) == 2


def test_tags_named_filters(db: Database, normal_user: User) -> None:
    """Test to retrieve tags for a specific user with named filters.

    Should retrieve tags for the user in the context based on specific named
    filters.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        normal_user: the model for the normal user.
    """
    with Context(user=normal_user) as c:
        # Test specific match
        tags = c.tags.get(title='test_daryl_2')
        assert tags[0].title == 'test_daryl_2'
        assert len(tags) == 1

        # Test if something that is invalid is not found indeed
        tags = c.tags.get(title='not_a_real_tag')
        assert len(tags) == 0

        # Test if a invalid field results in a exception
        with raises(InvalidFilterFieldException):
            tags = c.tags.get(unknown_field='test')
