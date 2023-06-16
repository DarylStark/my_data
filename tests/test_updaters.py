"""Tests for the updater of the ResourceManager.

Module that contains tests for the updaters of the ResourceManager.
"""
from my_model.user import User, UserRole
from my_model.tag import Tag

from database.database import Database
from my_data.context import Context
from my_data.exceptions import PermissionDeniedException

from pytest import raises


def test_update_users_normal(db: Database,
                             normal_user: User,
                             root_user: User) -> None:
    """Test to update (non-self) users as a normal user.

    Tries to updates a user as a normal user. This should fail; normal users
    are not allowed to update users, other than themselves. Because we cannot
    retrieve other users then the own user using the `getter`, we need to
    retrieve the user account via the root user first.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        normal_user: the model for the normal user.
        root_user: the model for the root user.
    """
    with Context(user=root_user) as local_context:
        user = local_context.users.get(username='root')

    with Context(user=normal_user) as local_context:
        with raises(PermissionDeniedException):
            user[0].username = 'root_new'
            local_context.users.update(user[0])


def test_update_tags_wrong_user(db: Database,
                                normal_user: User,
                                root_user: User) -> None:
    """Test to update tags from a different user.

    When a user tries to update a tag that is not theirs, the library has to
    raise a PermissionDeniedException error. We check if that happends in this
    unit test.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        normal_user: the model for the normal user.
        root_user: the model for the root user.
    """
    with Context(user=root_user) as local_context:
        tags = local_context.tags.get()

    with Context(user=normal_user) as local_context:
        with raises(PermissionDeniedException):
            tags[0].title = 'root_new'
            tag = local_context.tags.update(tags[0])


def test_update_own_user_normal(db: Database, normal_user: User) -> None:
    """Test to update the own useraccount as a normal user.

    Tries to updates the own user account for a normal user. This should not
    fail; a user is allowed to change his own user account.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        normal_user: the model for the normal user.
    """
    with Context(user=normal_user) as local_context:
        user = local_context.users.get()
        user[0].username = 'daryl.stark_updated'
        user = local_context.users.update(user[0])

        # Check the return type
        assert isinstance(user, User), "Wrong returntype"

    # Check if the resource is updated
    with Context(user=normal_user) as local_context:
        users = local_context.users.get()
        assert len(users) == 1
        assert users[0].username == 'daryl.stark_updated'


def test_update_users_root(db: Database, root_user: User) -> None:
    """Test to update users as a root user.

    Tries to updates a user as a root user. This shouldn't fail; root users are
    allowed to update users.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        root_user: the model for the root user.
    """
    with Context(user=root_user) as local_context:
        user = local_context.users.get(username='daryl.stark')
        user[0].username = 'daryl.stark_updated'
        user = local_context.users.update(user[0])

        # Check the return type
        assert isinstance(user, User), "Wrong returntype"

    # Check if the resource is updated
    with Context(user=root_user) as local_context:
        users = local_context.users.get(username='daryl.stark_updated')
        assert len(users) == 1
        assert users[0].username == 'daryl.stark_updated'


def test_update_tags(db: Database, normal_user: User) -> None:
    """Test to update a tag.

    Tries to update a tag for a normal user. This should work perfectly since
    a user is allowed to update his own tags.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        normal_user: the model for the normal user.
    """
    with Context(user=normal_user) as local_context:
        tag = local_context.tags.get(title='test_daryl_1')[0]
        tag.title = 'test_daryl_1_edited'
        tag = local_context.tags.update(tag)

        # Check the return type
        assert isinstance(tag, Tag), "Wrong returntype"

    # Check if the resource is added
    with Context(user=normal_user) as local_context:
        tags = local_context.tags.get(title='test_daryl_1_edited')
        assert len(tags) == 1
        assert tag.title == 'test_daryl_1_edited'
