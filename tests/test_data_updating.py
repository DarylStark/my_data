"""Unit tests to update data in the database.

This module contains unit tests that update data in the database. After the
update, it checks if the data has been updated.
"""
from my_model.user_scoped_models import (APIClient, APIToken, Tag, User,
                                         UserSetting)
from pytest import mark, raises

from my_data.exceptions import PermissionDeniedException
from my_data.my_data import MyData

pytestmark = mark.updating


def test_data_updating_own_user_as_root(
        my_data: MyData,
        root_user: User) -> None:
    """Test updating the own user as a ROOT user.

    Updates the own user as a ROOT user. Should always be succesfull since the
    root user can update all users.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
    """
    with my_data.get_context(user=root_user) as context:
        # Get the root user
        user = context.users.retrieve(User.username ==  # type:ignore
                                      'root')[0]

        # Update the password
        user.set_password('test')

        # Save it to the database
        context.users.update(user)

        # Get the user again
        user = context.users.retrieve(User.username ==  # type:ignore
                                      'root')[0]

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
        user = context.users.retrieve(User.username ==  # type:ignore
                                      'normal.user.1')[0]

        # Update the password
        user.set_password('test')

        # Save it to the database
        context.users.update(user)

        # Get the user again
        user = context.users.retrieve(User.username ==  # type:ignore
                                      'normal.user.1')[0]

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
            User.username ==  # type:ignore
            normal_user_1.username)[0]

        # Update the password
        user.set_password('test')

        # Save it to the database
        context.users.update(user)

        # Get the user again
        user = context.users.retrieve(
            User.username ==  # type:ignore
            normal_user_1.username)[0]

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
        user = context.users.retrieve(User.username ==  # type:ignore
                                      'root')[0]

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
        tag = context.tags.retrieve(Tag.title ==  # type:ignore
                                    'root_tag_1_new')[0]
        assert tag.title == 'root_tag_1_new'

        # Reset the title again
        tag.title = old_title
        context.tags.update(tag)


def test_data_updating_tag_as_normal_user_1(
        my_data: MyData,
        normal_user_1: User) -> None:
    """Test updating a user as a USER user.

    Updates a tag as a USER user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_1: the normal user for the context.
    """
    with my_data.get_context(user=normal_user_1) as context:
        # Get the first tag for this user
        tag = context.tags.retrieve()[0]
        old_title = tag.title

        # Update the title
        tag.title = 'normal_user_1_tag_1_new'

        # Save it to the database
        context.tags.update(tag)

        # Get the tag again and check the title
        tag = context.tags.retrieve(Tag.title ==  # type:ignore
                                    'normal_user_1_tag_1_new')[0]
        assert tag.title == 'normal_user_1_tag_1_new'

        # Reset the title again
        tag.title = old_title
        context.tags.update(tag)


def test_data_updating_api_client_as_root(
        my_data: MyData,
        root_user: User) -> None:
    """Test updating a API Client as a ROOT user.

    Updates a API Client as a ROOT user.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
    """
    with my_data.get_context(user=root_user) as context:
        # Get the first client for this user
        api_client = context.api_clients.retrieve()[0]
        old_name = api_client.app_name

        # Update the name
        api_client.app_name = 'root_api_client_1_new'

        # Save it to the database
        context.api_clients.update(api_client)

        # Get the client again and check the title
        api_client = context.api_clients.retrieve(
            APIClient.app_name ==  # type:ignore
            'root_api_client_1_new')[0]
        assert api_client.app_name == 'root_api_client_1_new'

        # Reset the name again
        api_client.app_name = old_name
        context.api_clients.update(api_client)


def test_data_updating_api_client_as_normal_user_1(
        my_data: MyData,
        normal_user_1: User) -> None:
    """Test updating a API Client as a USER user.

    Updates a API Client as a USER user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_1: the normal user for the context.
    """
    with my_data.get_context(user=normal_user_1) as context:
        # Get the first client for this user
        api_client = context.api_clients.retrieve()[0]
        old_name = api_client.app_name

        # Update the name
        api_client.app_name = 'normal_user_1_api_client_1_new'

        # Save it to the database
        context.api_clients.update(api_client)

        # Get the client again and check the title
        api_client = context.api_clients.retrieve(
            APIClient.app_name ==  # type:ignore
            'normal_user_1_api_client_1_new')[0]
        assert api_client.app_name == 'normal_user_1_api_client_1_new'

        # Reset the name again
        api_client.app_name = old_name
        context.api_clients.update(api_client)


def test_data_updating_api_token_as_root(
        my_data: MyData,
        root_user: User) -> None:
    """Test updating a API Token as a ROOT user.

    Updates a API Token as a ROOT user.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
    """
    with my_data.get_context(user=root_user) as context:
        # Get the first token for this user
        api_token = context.api_tokens.retrieve()[0]
        old_title = api_token.title

        # Update the title
        api_token.title = 'root_api_token_1_new'

        # Save it to the database
        context.api_tokens.update(api_token)

        # Get the token again and check the title
        api_token = context.api_tokens.retrieve(
            APIToken.title ==  # type:ignore
            'root_api_token_1_new')[0]
        assert api_token.title == 'root_api_token_1_new'

        # Reset the name again
        api_token.title = old_title
        context.api_tokens.update(api_token)


def test_data_updating_api_token_as_normal_user_1(
        my_data: MyData,
        normal_user_1: User) -> None:
    """Test updating a API token as a USER user.

    Updates a API token as a USER user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_1: the normal user for the context.
    """
    with my_data.get_context(user=normal_user_1) as context:
        # Get the first token for this user
        api_token = context.api_tokens.retrieve()[0]
        old_title = api_token.title

        # Update the title
        api_token.title = 'normal_user_1_api_token_1_new'

        # Save it to the database
        context.api_tokens.update(api_token)

        # Get the token again and check the title
        api_token = context.api_tokens.retrieve(
            APIToken.title ==  # type:ignore
            'normal_user_1_api_token_1_new')[0]
        assert api_token.title == 'normal_user_1_api_token_1_new'

        # Reset the name again
        api_token.title = old_title
        context.api_tokens.update(api_token)


def test_data_updating_user_setting_as_root(
        my_data: MyData,
        root_user: User) -> None:
    """Test updating a User Setting as a ROOT user.

    Updates a User Setting  as a ROOT user.

    Args:
        my_data: a instance of a MyData object.
        root_user: the root user for the context.
    """
    with my_data.get_context(user=root_user) as context:
        # Get the User Setting for this user
        user_setting = context.user_settings.retrieve()[0]
        old_value = user_setting.value

        # Update the value
        user_setting.value = 'test_value_new'

        # Save it to the database
        context.user_settings.update(user_setting)

        # Get the setting again and check the value
        user_setting = context.user_settings.retrieve(
            UserSetting.value == 'test_value_new')[0]  # type:ignore
        assert user_setting.value == 'test_value_new'

        # Reset the name again
        user_setting.value = old_value
        context.user_settings.update(user_setting)


def test_data_updating_user_setting_as_normal_user_1(
        my_data: MyData,
        normal_user_1: User) -> None:
    """Test updating a User Setting  as a USER user.

    Updates a User Setting  as a USER user.

    Args:
        my_data: a instance of a MyData object.
        normal_user_1: the normal user for the context.
    """
    with my_data.get_context(user=normal_user_1) as context:
        # Get the User Setting for this user
        user_setting = context.user_settings.retrieve()[0]
        old_value = user_setting.value

        # Update the value
        user_setting.value = 'test_value_new'

        # Save it to the database
        context.user_settings.update(user_setting)

        # Get the setting again and check the value
        user_setting = context.user_settings.retrieve(
            UserSetting.value == 'test_value_new')[0]  # type:ignore
        assert user_setting.value == 'test_value_new'

        # Reset the name again
        user_setting.value = old_value
        context.user_settings.update(user_setting)
