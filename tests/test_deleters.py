"""Tests for the deleter of the ResourceManager.

Module that contains tests for the deleters of the ResourceManager.
"""
from my_model.user import User, UserRole
from my_model.tag import Tag
from pytest import raises

from database.database import Database
from my_data.context import Context
from my_data.exceptions import PermissionDeniedException


def test_delete_users_normal(db: Database, normal_user: User) -> None:
    """Test to delete users as a normal user.

    Tries to remove a user as a normal user. This should fail; normal users are
    not allowed to delete users. Not even their own account.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        normal_user: the model for the normal user.
    """
    with Context(user=normal_user) as local_context:
        with raises(PermissionDeniedException):
            users = local_context.users.get()
            for user in users:
                local_context.users.delete(user)


def test_delete_users_root(db: Database, root_user: User) -> None:
    """Test to deleter users as a root user.

    Tries to delete a user as a root user. This shouldn't fail; root users are
    allowed to delete users. Because we don't want to change the test-database
    for other unit tests, we create the user first.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        root_user: the model for the root user.
    """
    # Create a test user
    with Context(user=root_user) as local_context:
        created_users = local_context.users.create(User(
            fullname='Test User',
            email='test.user@my-daryl-stark.nl',
            username='test.user.test_delete_users_root',
            role=UserRole.USER
        ))

    # Remove the user
    with Context(user=root_user) as local_context:
        local_context.users.delete(created_users[0])

    # Check if the resource is deleted from the database
    with Context(user=root_user) as local_context:
        users = local_context.users.get(
            username='test.user.test_delete_users_root')
        assert len(users) == 0, "User was not deleted"


def test_delete_tags(db: Database, normal_user: User) -> None:
    """Test to delete tags.

    Removes a tag for a normal user. After removing it, the test checks if the
    tag is really deleted. To no interfere with the other unit tests, we create
    the tag first.

    Args:
        db: the database connection. Not used right now, but still in there to
            make sure the database is connected.
        normal_user: the model for the normal user.
    """
    # Create the test tag
    with Context(user=normal_user) as local_context:
        created_tag = local_context.tags.create(
            Tag(title='test.tag.test_delete_tags'))

    # Delete the test tag
    with Context(user=normal_user) as local_context:
        local_context.tags.delete(created_tag)

    # Check if the tag is deleted
    with Context(user=normal_user) as local_context:
        tags = local_context.tags.get(title='test.tag.test_delete_tags')
        assert len(tags) == 0, "Tag was not deleted"
