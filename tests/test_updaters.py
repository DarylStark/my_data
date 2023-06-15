"""Tests for the updater of the ResourceManager.

Module that contains tests for the updaters of the ResourceManager.
"""
from my_model.user import User, UserRole
from my_model.tag import Tag

from database.database import Database
from my_data.context import Context
from my_data.exceptions import PermissionDeniedException

from pytest import raises


def test_update_users_normal(db: Database, normal_user: User) -> None:
    """Test to update (non-self) users as a normal user.

    Tries to updates a user as a normal user. This should fail; normal users
    are not allowed to update users, other than themselves.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        normal_user: the model for the normal user.
    """
    with Context(user=normal_user) as local_context:
        with raises(PermissionDeniedException):
            # TODO: Write test
            assert False, "Not implemented yet"


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
        with raises(PermissionDeniedException):
            # TODO: Write test
            assert False, "Not implemented yet"


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
        # TODO: Write test
        assert False

    # Check if the resource is updated
    with Context(user=root_user) as local_context:
        users = local_context.users.get()
        for user in users:
            # TODO: Write test
            assert False, "Not implemented yet"
        assert False, "User not found in database"


def test_tags(db: Database, normal_user: User) -> None:
    """Test to update a tag.

    Tries to update a tag for a normal user. This should work perfectly since
    a user is allowed to update his own tags.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        normal_user: the model for the normal user.
    """
    with Context(user=normal_user) as local_context:
        # TODO: Write test
        assert False

    # Check if the resource is added
    with Context(user=normal_user) as local_context:
        tags = local_context.tags.get()
        for tag in tags:
            # TODO: Write test
            assert False
        assert False, "Tag not found in database"
