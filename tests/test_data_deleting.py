"""Unit tests to delete data from the database.

This module contains unit tests that delete data from the database. After the
deletion, it checks if the data has been deleted.
"""
from pytest import raises

from my_data.exceptions import PermissionDeniedException
from my_data.my_data import MyData
from my_model import APIClient, APIToken, Tag, User, UserSetting


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
            User.username ==  # type:ignore
            'root')

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
            User.username ==  # type:ignore
            'deletion_test_user_user_1')

        # Delete the user
        context.users.delete(users)

        # Check if the user is deleted
        users = context.users.retrieve(
            User.username ==  # type:ignore
            'deletion_test_user_user_1')
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
            User.username ==  # type:ignore
            'normal.user.1')

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
            Tag.title ==  # type:ignore
            'test_deletion_tag_1')

        # Delete the user
        context.tags.delete(tags)

        # Check if the user is deleted
        tags = context.tags.retrieve(
            Tag.title ==  # type:ignore
            'test_deletion_tag_1')
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
            Tag.title ==  # type:ignore
            'test_deletion_tag_1')

        # Delete the user
        context.tags.delete(tags)

        # Check if the user is deleted
        tags = context.tags.retrieve(
            Tag.title ==  # type:ignore
            'test_deletion_tag_1')
        assert len(tags) == 0


def test_data_deleting_api_clients_as_root(
        my_data: MyData,
        root_user: User,
        test_api_client_to_delete: APIClient) -> None:
    """Test deleting API clients as the root user.

    Deletes API clients as the root user.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
        test_api_client_to_delete: a test API client to create and delete.
    """
    with my_data.get_context(user=root_user) as context:
        # Create a API client
        context.api_clients.create(test_api_client_to_delete)

        # Get the API client
        api_clients = context.api_clients.retrieve(
            APIClient.app_name ==  # type:ignore
            'test_deletion_api_client_1')

        # Delete the API client
        context.api_clients.delete(api_clients)

        # Check if the API client is deleted
        api_clients = context.api_clients.retrieve(
            APIClient.app_name ==  # type:ignore
            'test_deletion_api_client_1')
        assert len(api_clients) == 0


def test_data_deleting_api_clients_as_normal_user(
        my_data: MyData,
        normal_user_1: User,
        test_api_client_to_delete: APIClient) -> None:
    """Test deleting API clients as the root user.

    Deletes API clients as a normal user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_1: the first normal user.
        test_api_client_to_delete: a test API client to create and delete.
    """
    with my_data.get_context(user=normal_user_1) as context:
        # Create a API client
        context.api_clients.create(test_api_client_to_delete)

        # Get the API client
        api_clients = context.api_clients.retrieve(
            APIClient.app_name ==  # type:ignore
            'test_deletion_api_client_1')

        # Delete the API client
        context.api_clients.delete(api_clients)

        # Check if the API client is deleted
        api_clients = context.api_clients.retrieve(
            APIClient.app_name ==  # type:ignore
            'test_deletion_api_client_1')
        assert len(api_clients) == 0


def test_data_deleting_api_tokens_as_root(
        my_data: MyData,
        root_user: User,
        test_api_token_to_delete: APIToken) -> None:
    """Test deleting API clients as the root user.

    Deletes API clients as the root user.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
        test_api_token_to_delete: a test API token to create and delete.
    """
    with my_data.get_context(user=root_user) as context:
        # Create a API token
        context.api_tokens.create(test_api_token_to_delete)

        # Get the API token
        api_tokens = context.api_tokens.retrieve(
            APIToken.title ==  # type:ignore
            'test_deletion_api_token_1')

        # Delete the API token
        context.api_tokens.delete(api_tokens)

        # Check if the API token is deleted
        api_tokens = context.api_tokens.retrieve(
            APIToken.title ==  # type:ignore
            'test_deletion_api_token_1')
        assert len(api_tokens) == 0


def test_data_deleting_api_tokens_as_normal_user(
        my_data: MyData,
        normal_user_1: User,
        test_api_token_to_delete: APIToken) -> None:
    """Test deleting API tokens as the root user.

    Deletes API tokens as a normal user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_1: the first normal user.
        test_api_token_to_delete: a test API token to create and delete.
    """
    with my_data.get_context(user=normal_user_1) as context:
        # Create a API token
        context.api_tokens.create(test_api_token_to_delete)

        # Get the API token
        api_tokens = context.api_tokens.retrieve(
            APIToken.title ==  # type:ignore
            'test_deletion_api_token_1')

        # Delete the API token
        context.api_tokens.delete(api_tokens)

        # Check if the API token is deleted
        api_tokens = context.api_tokens.retrieve(
            APIToken.title ==  # type:ignore
            'test_deletion_api_token_1')
        assert len(api_tokens) == 0


def test_data_deleting_user_settings_as_root(
        my_data: MyData,
        root_user: User,
        test_user_setting_to_delete: UserSetting) -> None:
    """Test deleting User Settings as the root user.

    Deletes User Settings as the root user.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
        test_user_setting_to_delete: a test User Settings to create and
            delete.
    """
    with my_data.get_context(user=root_user) as context:
        # Create a User Setting
        context.user_settings.create(test_user_setting_to_delete)

        # Get the User Setting
        user_settings = context.user_settings.retrieve(
            UserSetting.setting ==  # type:ignore
            'test_deletion_user_setting_1')

        # Delete the User Setting
        context.user_settings.delete(user_settings)

        # Check if the API token is deleted
        user_settings = context.user_settings.retrieve(
            UserSetting.setting ==  # type:ignore
            'test_deletion_user_setting_1')
        assert len(user_settings) == 0


def test_data_deleting_user_settings_as_normal_user(
        my_data: MyData,
        normal_user_1: User,
        test_user_setting_to_delete: UserSetting) -> None:
    """Test deleting User Settings as a normal user.

    Deletes User Settings as a normal user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_1: the first normal user.
        test_user_setting_to_delete: a test User Settings to create and
            delete.
    """
    with my_data.get_context(user=normal_user_1) as context:
        # Create a User Setting
        context.user_settings.create(test_user_setting_to_delete)

        # Get the User Setting
        user_settings = context.user_settings.retrieve(
            UserSetting.setting ==  # type:ignore
            'test_deletion_user_setting_1')

        # Delete the User Setting
        context.user_settings.delete(user_settings)

        # Check if the API token is deleted
        user_settings = context.user_settings.retrieve(
            UserSetting.setting ==  # type:ignore
            'test_deletion_user_setting_1')
        assert len(user_settings) == 0
