"""Unit tests to create data in the database.

This module contains unit tests that create data in the database. After the
creation, it checks if the data has been created.
"""

from my_model.user_scoped_models import Tag, User
from pytest import raises
from sqlmodel import or_

from my_data import MyData
from my_data.exceptions import PermissionDeniedException


def test_data_creation_users_as_root(
        my_data: MyData,
        root_user: User,
        test_root_user: User,
        test_normal_user: User) -> None:
    """Test User creation as a ROOT user.

    Creates a user as a root user.

    Args:
        my_data: a instance to a MyData object.
        root_user: the root user for the context.
        test_root_user: a ROOT user to create.
        test_normal_user: a USER user to create.
    """
    with my_data.get_context(user=root_user) as context:
        # Create the users.
        context.users.create([test_root_user, test_normal_user])

        # Check if they exist
        created_users = context.users.retrieve(
            User.username.like('creation_test_%'))

        assert len(created_users) == 2
        assert created_users[0].username == 'creation_test_root_user_1'
        assert created_users[1].username == 'creation_test_user_user_1'


def test_data_creation_users_as_normal_user_1(
        my_data: MyData,
        normal_user_1: User,
        test_normal_user: User) -> None:
    """Test User creation as a USER user.

    Creates a user as a normal user. This should fail: normal users are not
    allowed to create users.

    Args:
        my_data: a instance to a MyData object.
        normal_user_1: the first normal user.
        test_normal_user: a USER user to create.
    """
    with raises(PermissionDeniedException):
        with my_data.get_context(user=normal_user_1) as context:
            context.users.create(test_normal_user)


def test_data_creation_users_as_normal_user_2(
        my_data: MyData,
        normal_user_2: User,
        test_normal_user: User) -> None:
    """Test User creation as a USER user.

    Creates a user as a normal user. This should fail: normal users are not
    allowed to create users.

    Args:
        my_data: a instance to a MyData object.
        normal_user_2: the first normal user.
        test_normal_user: a USER user to create.
    """
    with raises(PermissionDeniedException):
        with my_data.get_context(user=normal_user_2) as context:
            context.users.create(test_normal_user)


def test_data_creation_tags_as_root(
        my_data: MyData,
        root_user: User,
        test_tags) -> None:
    """Test Tag creation as a ROOT user.

    Creates a tag as a root user.

    Args:
        my_data: a instance to a MyData object.
        root_user: the root user for the context.
        test_tags: a list with tags to add.
    """
    with my_data.get_context(user=root_user) as context:
        context.tags.create(test_tags)

        # Check if they exist
        created_tags = context.tags.retrieve(
            Tag.title.like('test_creation_tag_%'))

        assert len(created_tags) == 3
        assert created_tags[0].title == 'test_creation_tag_1'
        assert created_tags[1].title == 'test_creation_tag_2'
        assert created_tags[1].title == 'test_creation_tag_3'


def test_data_creation_tag_as_normal_user_1(
        my_data: MyData,
        normal_user_1: User,
        test_tags) -> None:
    """Test User creation as a USER user.

    Creates a tag as a normal user.

    Args:
        my_data: a instance to a MyData object.
        normal_user_1: the first normal user.
        test_tags: a list with tags to add.
    """
    with my_data.get_context(user=normal_user_1) as context:
        context.tags.create(test_tags)

        # Check if they exist
        created_tags = context.tags.retrieve(
            Tag.title.like('test_creation_tag_%'))

        assert len(created_tags) == 3
        assert created_tags[0].title == 'test_creation_tag_1'
        assert created_tags[1].title == 'test_creation_tag_2'
        assert created_tags[1].title == 'test_creation_tag_3'


def test_data_creation_tag_as_normal_user_2(
        my_data: MyData,
        normal_user_2: User,
        test_tags) -> None:
    """Test User creation as a USER user.

    Creates a tag as a normal user.

    Args:
        my_data: a instance to a MyData object.
        normal_user_2: the first normal user.
        test_tags: a list with tags to add.
    """
    with my_data.get_context(user=normal_user_1) as context:
        context.tags.create(test_tags)

        # Check if they exist
        created_tags = context.tags.retrieve(
            Tag.title.like('test_creation_tag_%'))

        assert len(created_tags) == 3
        assert created_tags[0].title == 'test_creation_tag_1'
        assert created_tags[1].title == 'test_creation_tag_2'
        assert created_tags[1].title == 'test_creation_tag_3'
