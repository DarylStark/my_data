"""Unit tests to test the tasks for Service users.

This module tests the things a Service user needs to do, like retrieving
User objects or API tokens.
"""

import pytest
from my_data.exceptions import UnknownUserAccountError
from my_data.my_data import MyData
from pytest import raises


def test_retrieving_user_objects_by_username(my_data: MyData) -> None:
    """Unit test to retrieve a User object by the username.

    This unit test tries to log in with a Service user and retrieve a User
    object using the username for the user. This can be used by clients that
    need a user to login.

    Args:
        my_data: a instance of a MyData object.
    """
    with my_data.get_context_for_service_user() as context:
        user = context.get_user_account_by_username('normal.user.1')
        assert user is not None
        assert user.username == 'normal.user.1'


def test_retrieving_user_objects_by_username_wrong_user(
    my_data: MyData,
) -> None:
    """Unit test to retrieve a User object by the username.

    This unit test tries to log in with a Service user and retrieve a User
    object using the username for the user. This can be used by clients that
    need a user to login.

    Args:
        my_data: a instance of a MyData object.
    """
    with my_data.get_context_for_service_user() as context:
        with raises(UnknownUserAccountError):
            context.get_user_account_by_username('wrong.user.1')


def test_retrieving_user_objects_by_api_token(my_data: MyData) -> None:
    """Unit test to retrieve a User object by the API token.

    This unit test tries to log in with a Service user and retrieve a User
    object using a API token.

    Args:
        my_data: a instance of a MyData object.
    """
    with my_data.get_context_for_service_user() as context:
        user = context.get_user_account_by_api_token(
            'aRlIytpyz61JX2TvczLxJZUsRzk578pE'
        )
        assert user is not None
        assert user.username == 'normal.user.2'


def test_retrieving_user_objects_by_api_token_wrong_token(
    my_data: MyData,
) -> None:
    """Unit test to retrieve a User object by the API token.

    This unit test tries to log in with a Service user and retrieve a User
    object using a API token.

    Args:
        my_data: a instance of a MyData object.
    """
    with my_data.get_context_for_service_user() as context:
        with raises(UnknownUserAccountError):
            context.get_user_account_by_api_token('wrong_token')


def test_retrieving_token_objects_by_api_token(my_data: MyData) -> None:
    """Unit test to retrieve a APIToken object by the API token.

    This unit test tries to log in with a Service user and retrieve a APIToken
    object using a API token.

    Args:
        my_data: a instance of a MyData object.
    """
    with my_data.get_context_for_service_user() as context:
        token = context.get_api_token_object_by_api_token(
            'aRlIytpyz61JX2TvczLxJZUsRzk578pE'
        )
        assert token is not None
        assert token.user.username == 'normal.user.2'


def test_retrieving_token_objects_by_api_token_wrong_token(
    my_data: MyData,
) -> None:
    """Unit test to retrieve a APIToken object by the API token.

    This unit test tries to log in with a Service user and retrieve a User
    object using a API token. This should fail because the token is wrong.

    Args:
        my_data: a instance of a MyData object.
    """
    with my_data.get_context_for_service_user() as context:
        with raises(UnknownUserAccountError):
            context.get_api_token_object_by_api_token('wrong_token')


def test_retrieving_api_scopes(my_data: MyData) -> None:
    """Unit test to retrieve a APIScope objects.

    This unit test tries to log in with a Service user and retrieve a APIScope
    objects.

    Args:
        my_data: a instance of a MyData object.
    """
    with my_data.get_context_for_service_user() as context:
        scopes = context.get_api_scopes()
        assert scopes is not None
        assert len(scopes) == 9


@pytest.mark.parametrize('module', ['users'])
def test_retrieving_api_scopes_filtered_on_module(
    my_data: MyData, module: str
) -> None:
    """Unit test to retrieve a APIScope objects filtered on module.

    This unit test tries to log in with a Service user and retrieve a APIScope
    objects.

    Args:
        my_data: a instance of a MyData object.
        module: the module to filter on.
    """
    with my_data.get_context_for_service_user() as context:
        scopes = context.get_api_scopes(module=module)
        assert scopes is not None
        assert len(scopes) == 5


@pytest.mark.parametrize(
    'subject, count',
    [
        ['create', 2],
        ['retrieve', 2],
        ['update', 2],
        ['delete', 2],
        ['updatepw', 1],
    ],
)
def test_retrieving_api_scopes_filtered_on_subject(
    my_data: MyData, subject: str, count: int
) -> None:
    """Unit test to retrieve a APIScope objects filtered on subject.

    This unit test tries to log in with a Service user and retrieve a APIScope
    objects.

    Args:
        my_data: a instance of a MyData object.
        subject: the subject to filter on.
        count: the number of objects to expect.
    """
    with my_data.get_context_for_service_user() as context:
        scopes = context.get_api_scopes(subject=subject)
        assert scopes is not None
        assert len(scopes) == count


@pytest.mark.parametrize(
    'module, subject',
    [
        ('users', 'create'),
        ('users', 'retrieve'),
        ('users', 'update'),
        ('users', 'delete'),
        ('users', 'updatepw'),
        ('tags', 'create'),
        ('tags', 'retrieve'),
        ('tags', 'update'),
        ('tags', 'delete'),
    ],
)
def test_retrieving_api_scopes_filtered_on_module_and_subject(
    my_data: MyData, module: str, subject: str
) -> None:
    """Unit test to retrieve a APIScope objects filtered on module and subject.

    This unit test tries to log in with a Service user and retrieve a APIScope
    objects.

    Args:
        my_data: a instance of a MyData object.
        module: the module to filter on.
        subject: the subject to filter on.
    """
    with my_data.get_context_for_service_user() as context:
        scopes = context.get_api_scopes(module=module, subject=subject)
        assert scopes is not None
        assert len(scopes) == 1
