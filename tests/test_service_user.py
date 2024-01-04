"""Unit tests to test the tasks for Service users.

This module tests the things a Service user needs to do, like retrieving
User objects or API tokens.
"""
from pytest import mark, raises

from my_data.exceptions import UnknownUserAccountException  # type:ignore
from my_data.my_data import MyData  # type:ignore

pytestmark = mark.service_user


def test_retrieving_user_objects_by_username(my_data: MyData) -> None:
    """Unit test to retrieve a User object by the username.

    This unit test tries to log in with a Service user and retrieve a User
    object using the username for the user. This can be used by clients that
    need a user to login.

    Args:
        my_data: a instance of a MyData object.
    """
    with my_data.get_context_for_service_user(
            username='service.user',
            password='service_password') as context:
        user = context.get_user_account_by_username('normal.user.1')
        assert user is not None
        assert user.username == 'normal.user.1'


def test_retrieving_user_objects_by_username_wrong_user(
        my_data: MyData) -> None:
    """Unit test to retrieve a User object by the username.

    This unit test tries to log in with a Service user and retrieve a User
    object using the username for the user. This can be used by clients that
    need a user to login.

    Args:
        my_data: a instance of a MyData object.
    """
    with my_data.get_context_for_service_user(
            username='service.user',
            password='service_password') as context:
        with raises(UnknownUserAccountException):
            context.get_user_account_by_username('wrong.user.1')


def test_retrieving_user_objects_by_api_token(my_data: MyData) -> None:
    """Unit test to retrieve a User object by the API token.

    This unit test tries to log in with a Service user and retrieve a User
    object using a API token.

    Args:
        my_data: a instance of a MyData object.
    """
    with my_data.get_context_for_service_user(
            username='service.user',
            password='service_password') as context:
        user = context.get_user_account_by_api_token(
            'aRlIytpyz61JX2TvczLxJZUsRzk578pE')
        assert user is not None
        assert user.username == 'normal.user.2'


def test_retrieving_user_objects_by_api_token_wrong_token(
        my_data: MyData) -> None:
    """Unit test to retrieve a User object by the API token.

    This unit test tries to log in with a Service user and retrieve a User
    object using a API token.

    Args:
        my_data: a instance of a MyData object.
    """
    with my_data.get_context_for_service_user(
            username='service.user',
            password='service_password') as context:
        with raises(UnknownUserAccountException):
            context.get_user_account_by_api_token(
                'wrong_token')
