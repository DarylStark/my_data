"""Tests for the creator of the ResourceManager.

Module that contains tests for the creators of the ResourceManager.
"""
from my_model.user import User, UserRole
from my_model.tag import Tag

from database.database import Database
from my_data.context import Context
from my_data.exceptions import PermissionDeniedException

from pytest import raises


def test_create_users_normal(db: Database, normal_user: User) -> None:
    """Test to create users as a normal user.

    Tries to create a user as a normal user. This should fail; normal users are
    not allowed to create users.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        normal_user: the model for the normal user.
    """
    with Context(user=normal_user) as local_context:
        with raises(PermissionDeniedException):
            local_context.users.create(User(
                fullname='Test User',
                email='test.user@my-daryl-stark.nl',
                username='test.user',
                role=UserRole.USER
            ))


def test_create_users_root(db: Database, root_user: User) -> None:
    """Test to create users as a root user.

    Tries to create a user as a root user. This shouldn't fail; root users are
    allowed to create users.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        root_user: the model for the root user.
    """
    with Context(user=root_user) as local_context:
        local_context.users.create(User(
            fullname='Test User',
            email='test.user@my-daryl-stark.nl',
            username='test.user',
            role=UserRole.USER
        ))

    # Check if the resource is added
    with Context(user=root_user) as local_context:
        users = local_context.users.get()
        for user in users:
            if user.username == 'test.user':
                assert True
                return
        assert False, "User not found in database"


def test_create_tags(db: Database, normal_user: User) -> None:
    """Test to update a tag.

    Tries to create a tag for a normal user. This should work perfectly since
    a user is allowed to create tags for his own useraccount.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        normal_user: the model for the normal user.
    """
    with Context(user=normal_user) as local_context:
        local_context.tags.create(Tag(
            title='test'
        ))

    # Check if the resource is added
    with Context(user=normal_user) as local_context:
        tags = local_context.tags.get()
        for tag in tags:
            if tag.title == 'test':
                assert True
                return
        assert False, "Tag not found in database"
