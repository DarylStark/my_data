"""Unit tests to update data in the database.

This module contains unit tests that update data in the database. After the
update, is checks if the data has been updated.
"""
from my_model.user_scoped_models import User, Tag
from pytest import raises

from my_data.exceptions import PermissionDeniedException
from my_data.my_data import MyData


def test_data_updating_own_user_as_root(
        my_data: MyData,
        root_user: User) -> None:
    """Test updating the own user as a ROOT user.

    Updates the ownuser as a ROOT user. Should always be succesfull since the
    root user can update all users.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
    """
    with my_data.get_context(user=root_user) as context:
        # Get the root user
        user = context.users.retrieve(User.username == 'root')[0]

        # Update the password
        user.set_password('test')

        # Save it to the database
        context.users.update(user)

        # Get the user again
        user = context.users.retrieve(User.username == 'root')[0]

        # Check the password
        assert user.verify_credentials('root', 'test')


def test_data_updating_other_user_as_root(
        my_data: MyData,
        root_user: User) -> None:
    """Test updating a other user as a ROOT user.

    Updates a other user as a ROOT user. Should always be succesfull since the
    root user can update all users.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
    """
    with my_data.get_context(user=root_user) as context:
        # Get the root user
        user = context.users.retrieve(User.username == 'normal.user.1')[0]

        # Update the password
        user.set_password('test')

        # Save it to the database
        context.users.update(user)

        # Get the user again
        user = context.users.retrieve(User.username == 'normal.user.1')[0]

        # Check the password
        assert user.verify_credentials('normal.user.1', 'test')


def test_data_updating_own_user_as_normal_user_1(
        my_data: MyData,
        normal_user_1: User) -> None:
    """Test updating the own user as a USER user.

    Updates the current user as a normal user. Should be successfull since the
    user can update his own account.

    Args:
        my_data: a instance of a MyData object.
        normal_user_1: the first normal user.
    """
    with my_data.get_context(user=normal_user_1) as context:
        # Get the root user
        user = context.users.retrieve(
            User.username == normal_user_1.username)[0]

        # Update the password
        user.set_password('test')

        # Save it to the database
        context.users.update(user)

        # Get the user again
        user = context.users.retrieve(
            User.username == normal_user_1.username)[0]

        # Check the password
        assert user.verify_credentials(normal_user_1.username, 'test')


def test_data_updating_other_user_as_normal_user_1(
        my_data: MyData,
        root_user: User,
        normal_user_1: User) -> None:
    """Test updating a other user as a USER user.

    Updates the a othre user as a normal user. Should not be successfull since
    normal users can only update their own user account.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
        normal_user_1: the first normal user.
    """

    with my_data.get_context(user=root_user) as context:
        # Get the root user. We have to do this in a context with the root user
        # as the user, otherwide we won't get the user account.
        user = context.users.retrieve(User.username == 'root')[0]

    with my_data.get_context(user=normal_user_1) as context:
        # Update the password
        user.set_password('test')

        # Save it to the database
        with raises(PermissionDeniedException):
            context.users.update(user)


def test_data_updating_tag_as_root(
        my_data: MyData,
        root_user: User) -> None:
    """Test updating a user as a ROOT user.

    Updates a tag as a ROOT user.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
    """
    with my_data.get_context(user=root_user) as context:
        # Get the first tag for this user
        tag = context.tags.retrieve()[0]
        old_title = tag.title

        # Update the title
        tag.title = 'root_tag_1_new'

        # Save it to the database
        context.tags.update(tag)

        # Get the tag again and check the title
        tag = context.tags.retrieve(Tag.title == 'root_tag_1_new')[0]
        assert tag.title == 'root_tag_1_new'

        # Reset the title again
        tag.title = old_title
        context.tags.update(tag)


def test_data_updating_tag_as_normal_user_1(
        my_data: MyData,
        normal_user_1: User) -> None:
    with my_data.get_context(user=normal_user_1) as context:
        # Get the first tag for this user
        tag = context.tags.retrieve()[0]
        old_title = tag.title

        # Update the title
        tag.title = 'normal_user_1_tag_1_new'

        # Save it to the database
        context.tags.update(tag)

        # Get the tag again and check the title
        tag = context.tags.retrieve(Tag.title == 'normal_user_1_tag_1_new')[0]
        assert tag.title == 'normal_user_1_tag_1_new'

        # Reset the title again
        tag.title = old_title
        context.tags.update(tag)
