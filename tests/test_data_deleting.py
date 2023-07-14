"""Unit tests to delete data from the database.

This module contains unit tests that delete data from the database. After the
deletion, it checks if the data has been deleted.
"""
from my_model.user_scoped_models import User, Tag
from pytest import raises
from my_data.exceptions import PermissionDeniedException

from my_data.my_data import MyData


def test_data_deleting_own_user_as_root(
        my_data: MyData,
        root_user: User) -> None:
    """Test deleting the own user as a ROOT user.

    Deletes the own user as a ROOT user. Should always fail cause the own user
    is not to be removed.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
    """
    with my_data.get_context(user=root_user) as context:
        # Get the user
        users = context.users.retrieve(
            User.username == 'root')

        # Delete the user. This should give an error
        with raises(PermissionDeniedException):
            context.users.delete(users[0])


def test_data_deleting_other_user_as_root(
        my_data: MyData,
        root_user: User,
        test_normal_user_to_delete: User) -> None:
    """Test deleting a other user as a ROOT user.

    Deleters a other user as a ROOT user. Should always be successfull since
    the ROOT user can delete all users.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
        test_normal_user_to_delete: a user to create and delete.
    """
    with my_data.get_context(user=root_user) as context:
        # Create a testuser
        context.users.create(test_normal_user_to_delete)

        # Get the user
        users = context.users.retrieve(
            User.username == 'deletion_test_user_user_1')

        # Delete the user
        context.users.delete(users)

        # Check if the user is deleted
        users = context.users.retrieve(
            User.username == 'deletion_test_user_user_1')
        assert len(users) == 0


def test_data_deleting_own_user_as_normal_user(
        my_data: MyData,
        normal_user_1: User) -> None:
    """Test deleting the own user as a USER user.

    Deletes the own user as a USER user. Should always fail cause the own user
    is not to be removed.

    Args:
        my_data: a instance of a MyData object.
        normal_user_1: the first normal user.
    """
    with my_data.get_context(user=normal_user_1) as context:
        # Get the user
        users = context.users.retrieve(
            User.username == 'normal.user.1')

        # Delete the user. This should give an error
        with raises(PermissionDeniedException):
            context.users.delete(users[0])


def test_data_deleting_tags_as_root(
        my_data: MyData,
        root_user: User,
        test_tag_to_delete: Tag) -> None:
    """Test deleting tags as the root user.

    Deletes tags as the root user.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
        test_tag_to_delete: a test tag to create and delete.
    """
    with my_data.get_context(user=root_user) as context:
        # Create a testtag
        context.tags.create(test_tag_to_delete)

        # Get the tag
        tags = context.tags.retrieve(
            User.username == 'test_deletion_tag_1')

        # Delete the user
        context.tags.delete(tags)

        # Check if the user is deleted
        tags = context.tags.retrieve(
            User.username == 'test_deletion_tag_1')
        assert len(tags) == 0


def test_data_deleting_tags_as_normal_user(
        my_data: MyData,
        normal_user_1: User,
        test_tag_to_delete: Tag) -> None:
    """Test deleting tags as the root user.

    Deletes tags as a normal user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_1: the first normal user.
        test_tag_to_delete: a test tag to create and delete.
    """
    with my_data.get_context(user=normal_user_1) as context:
        # Create a testtag
        context.tags.create(test_tag_to_delete)

        # Get the tag
        tags = context.tags.retrieve(
            User.username == 'test_deletion_tag_1')

        # Delete the user
        context.tags.delete(tags)

        # Check if the user is deleted
        tags = context.tags.retrieve(
            User.username == 'test_deletion_tag_1')
        assert len(tags) == 0
