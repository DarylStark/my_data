"""Tests for the getters of the ResourceManager.

Module that contains tests for the getters of the ResourceManager.
"""
from my_model.user_scoped_models import Tag, User
from pytest import raises

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
    with Context(user=normal_user) as local_context:
        users = local_context.users.get()
        assert (users[0].username == 'daryl.stark')
        assert (len(users) == 1)

        # Check the return types
        for user in users:
            assert isinstance(user, User), "Wrong returntype"


def test_get_users_root(db: Database, root_user: User) -> None:
    """Test to retrieve users as a root user.

    Retrieves user in a root user context. Should retrieve all users in the
    database.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        root_user: the model for the root user.
    """
    with Context(user=root_user) as local_context:
        users = local_context.users.get()
        assert (users[0].username == 'root')
        assert (users[1].username == 'daryl.stark')
        assert (len(users) == 2)

        # Check the return types
        for user in users:
            assert isinstance(user, User), "Wrong returntype"


def test_get_tags(db: Database, normal_user: User) -> None:
    """Test to retrieve tags for a specific user.

    Should retrieve all tags that are created in the test database for the
    specific user.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        normal_user: the model for the normal user.
    """
    with Context(user=normal_user) as local_context:
        tags = local_context.tags.get()
        assert len(tags) == 2
        assert tags[0].title == 'test_daryl_1'
        assert tags[1].title == 'test_daryl_2'

        # Check the return types
        for tag in tags:
            assert isinstance(tag, Tag), "Wrong returntype"


def test_get_users_filter(db: Database, root_user: User) -> None:
    """Test to retrieve users as root with a raw filter.

    Should retrieve users the context based on specific raw filters.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        root_user: the model for the root user.
    """
    with Context(user=root_user) as local_context:
        # Test specific match
        users = local_context.users.get(
            filter=[User.username == 'root'])
        assert users[0].username == 'root'
        assert len(users) == 1

        # Check the return types
        for user in users:
            assert isinstance(user, User), "Wrong returntype"

        # Test specific unmatch
        users = local_context.users.get(
            filter=[User.username != 'root'])
        assert users[0].username == 'daryl.stark'
        assert len(users) == 1

        # Check the return types
        for user in users:
            assert isinstance(user, User), "Wrong returntype"

        # Test bigger then
        users = local_context.users.get(filter=[User.id > 0])
        assert users[0].username == 'root'
        assert users[1].username == 'daryl.stark'
        assert len(users) == 2

        # Check the return types
        for user in users:
            assert isinstance(user, User), "Wrong returntype"

        # Test smaller then
        users = local_context.users.get(filter=[User.id < 99])
        assert users[0].username == 'root'
        assert users[1].username == 'daryl.stark'
        assert len(users) == 2

        # Check the return types
        for user in users:
            assert isinstance(user, User), "Wrong returntype"


def test_get_tags_filter(db: Database, normal_user: User) -> None:
    """Test to retrieve tags for a specific user with a raw filter.

    Should retrieve tags for the user in the context based on specific raw
    filters.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        normal_user: the model for the normal user.
    """
    with Context(user=normal_user) as local_context:
        # Test specific match
        tags = local_context.tags.get(
            filter=[Tag.title == 'test_daryl_2'])
        assert tags[0].title == 'test_daryl_2'
        assert len(tags) == 1

        # Check the return types
        for tag in tags:
            assert isinstance(tag, Tag), "Wrong returntype"

        # Test specific unmatch
        tags = local_context.tags.get(
            filter=[Tag.title != 'test_daryl_2'])
        assert tags[0].title == 'test_daryl_1'
        assert len(tags) == 1

        # Check the return types
        for tag in tags:
            assert isinstance(tag, Tag), "Wrong returntype"

        # Test bigger then
        tags = local_context.tags.get(filter=[Tag.id > 0])
        assert tags[0].title == 'test_daryl_1'
        assert tags[1].title == 'test_daryl_2'
        assert len(tags) == 2

        # Check the return types
        for tag in tags:
            assert isinstance(tag, Tag), "Wrong returntype"

        # Test smaller then
        tags = local_context.tags.get(filter=[Tag.id < 999])
        assert tags[0].title == 'test_daryl_1'
        assert tags[1].title == 'test_daryl_2'
        assert len(tags) == 2

        # Check the return types
        for tag in tags:
            assert isinstance(tag, Tag), "Wrong returntype"
