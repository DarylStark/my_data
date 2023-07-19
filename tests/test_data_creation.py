"""Unit tests to create data in the database.

This module contains unit tests that create data in the database. After the
creation, it checks if the data has been created.
"""

from my_model.user_scoped_models import Tag, User, APIClient
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
        my_data: a instance of a MyData object.
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
        my_data: a instance of a MyData object.
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
        my_data: a instance of a MyData object.
        normal_user_2: the first normal user.
        test_normal_user: a USER user to create.
    """
    with raises(PermissionDeniedException):
        with my_data.get_context(user=normal_user_2) as context:
            context.users.create(test_normal_user)


def test_data_creation_tags_as_root(
        my_data: MyData,
        root_user: User,
        test_tags: list[Tag]) -> None:
    """Test Tag creation as a ROOT user.

    Creates a tag as a root user.

    Args:
        my_data: a instance of a MyData object.
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
        assert created_tags[2].title == 'test_creation_tag_3'


def test_data_creation_tag_as_normal_user_1(
        my_data: MyData,
        normal_user_1: User,
        test_tags: list[Tag]) -> None:
    """Test User creation as a USER user.

    Creates a tag as a normal user.

    Args:
        my_data: a instance of a MyData object.
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
        assert created_tags[2].title == 'test_creation_tag_3'


def test_data_creation_tag_as_normal_user_2(
        my_data: MyData,
        normal_user_2: User,
        test_tags: list[Tag]) -> None:
    """Test User creation as a USER user.

    Creates a tag as a normal user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_2: the first normal user.
        test_tags: a list with tags to add.
    """
    with my_data.get_context(user=normal_user_2) as context:
        context.tags.create(test_tags)

        # Check if they exist
        created_tags = context.tags.retrieve(
            Tag.title.like('test_creation_tag_%'))

        assert len(created_tags) == 3
        assert created_tags[0].title == 'test_creation_tag_1'
        assert created_tags[1].title == 'test_creation_tag_2'
        assert created_tags[2].title == 'test_creation_tag_3'


def test_data_creation_tag_as_normal_user_1_wrong_user_id(
        my_data: MyData,
        normal_user_2: User,
        test_tags: list[Tag]) -> None:
    """Test User creation as a USER user.

    Creates a tag as a normal user with a wrong User ID. Should raise an
    PermissionDeniedException exception.

    Args:
        my_data: a instance of a MyData object.
        normal_user_2: the first normal user.
        test_tags: a list with tags to add.
    """
    with my_data.get_context(user=normal_user_2) as context:
        with raises(PermissionDeniedException):
            # Set the wrong user IDs
            for tag in test_tags:
                tag.user_id = 1
            context.tags.create(test_tags)


def test_data_creation_api_clients_as_root(
        my_data: MyData,
        root_user: User,
        test_api_clients: list[APIClient]) -> None:
    """Test API Client creation as a ROOT user.

    Creates a API client as a root user.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
        test_api_clients: a list with API clients to add.
    """
    with my_data.get_context(user=root_user) as context:
        context.api_clients.create(test_api_clients)

        # Check if they exist
        created_api_clients = context.api_clients.retrieve(
            APIClient.app_name.like('test_creation_api_client_%'))

        assert len(created_api_clients) == 3
        assert created_api_clients[0].app_name == 'test_creation_api_client_1'
        assert created_api_clients[1].app_name == 'test_creation_api_client_2'
        assert created_api_clients[2].app_name == 'test_creation_api_client_3'


def test_data_creation_api_clients_as_normal_user_1(
        my_data: MyData,
        normal_user_1: User,
        test_api_clients: list[APIClient]) -> None:
    """Test User creation as a USER user.

    Creates a API client as a normal user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_1: the first normal user.
        test_api_clients: a list with API clients to add.
    """
    with my_data.get_context(user=normal_user_1) as context:
        context.api_clients.create(test_api_clients)

        # Check if they exist
        created_api_clients = context.api_clients.retrieve(
            APIClient.app_name.like('test_creation_api_client_%'))

        assert len(created_api_clients) == 3
        assert created_api_clients[0].app_name == 'test_creation_api_client_1'
        assert created_api_clients[1].app_name == 'test_creation_api_client_2'
        assert created_api_clients[2].app_name == 'test_creation_api_client_3'


def test_data_creation_api_clients_as_normal_user_2(
        my_data: MyData,
        normal_user_2: User,
        test_api_clients: list[APIClient]) -> None:
    """Test User creation as a USER user.

    Creates a API client as a normal user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_2: the first normal user.
        test_api_clients: a list with API clients to add.
    """
    with my_data.get_context(user=normal_user_2) as context:
        context.api_clients.create(test_api_clients)

        # Check if they exist
        created_api_clients = context.api_clients.retrieve(
            APIClient.app_name.like('test_creation_api_client_%'))

        assert len(created_api_clients) == 3
        assert created_api_clients[0].app_name == 'test_creation_api_client_1'
        assert created_api_clients[1].app_name == 'test_creation_api_client_2'
        assert created_api_clients[2].app_name == 'test_creation_api_client_3'


def test_data_creation_api_clients_as_normal_user_1_wrong_user_id(
        my_data: MyData,
        normal_user_2: User,
        test_api_clients: list[APIClient]) -> None:
    """Test User creation as a USER user.

    Creates a API client as a normal user with a wrong User ID. Should raise an
    PermissionDeniedException exception.

    Args:
        my_data: a instance of a MyData object.
        normal_user_2: the first normal user.
        test_api_clients: a list with API clients to add.
    """
    with my_data.get_context(user=normal_user_2) as context:
        with raises(PermissionDeniedException):
            # Set the wrong user IDs
            for api_client in test_api_clients:
                api_client.user_id = 1
            context.api_clients.create(test_api_clients)
