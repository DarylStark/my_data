"""Tests for the Authenticator class and it's authenticators."""
# ruff: noqa: SLF001

import pytest
from my_data import MyData
from my_data.authenticator import CredentialsAuthenticator, UserAuthenticator
from my_data.exceptions import (
    AuthenticationFailedError,
    AuthenticatorNotConfiguredError,
    UserAuthenticatorAlreadySetError,
)
from my_model import APIToken, User


def test_creating_user_authenticator(my_data: MyData) -> None:
    """Test creating a UserAuthenticator with a Authenticator.

    After doing this, the `_user_authenticator` attribute of the authenticator
    should be set to the UserAuthenticator.

    Args:
        my_data: a instance of a MyData object.
    """
    credentials_authenticator = CredentialsAuthenticator(
        username='normal.user.1',
        password='normal_user_1_pw',
        second_factor=None,
    )
    user_authenticator = UserAuthenticator(
        my_data_object=my_data, authenticator=credentials_authenticator
    )

    assert credentials_authenticator._user_authenticator is user_authenticator


def test_setting_authenticator_again(my_data: MyData) -> None:
    """Test setting a authenticator when it is already set.

    Should raise a UserAuthenticatorAlreadySetException exception.

    Args:
        my_data: a instance of a MyData object.
    """
    credentials_authenticator = CredentialsAuthenticator(
        username='normal.user.1',
        password='normal_user_1_pw',
        second_factor=None,
    )
    user_authenticator = UserAuthenticator(
        my_data_object=my_data, authenticator=credentials_authenticator
    )

    with pytest.raises(UserAuthenticatorAlreadySetError):
        credentials_authenticator.set_user_authenticator(user_authenticator)


@pytest.mark.parametrize(
    'user_id, username, password, second_factor',
    [
        (1, 'root', 'root_pw', None),
        (2, 'normal.user.1', 'normal_user_1_pw', None),
        (3, 'normal.user.2', 'normal_user_2_pw', None),
    ],
)
def test_credentials_authenticator_valid_credentials(
    my_data: MyData,
    user_id: int,
    username: str,
    password: str,
    second_factor: str,
) -> None:
    """Test authenticating with a valid credentials authenticator.

    Args:
        my_data: a instance of a MyData object.
        user_id: the id of the user to test with.
        username: the username to test with.
        password: the password to test with.
        second_factor: the second factor to test with.
    """
    credentials_authenticator = CredentialsAuthenticator(
        username=username, password=password, second_factor=second_factor
    )
    user_authenticator = UserAuthenticator(
        my_data_object=my_data, authenticator=credentials_authenticator
    )
    user = user_authenticator.authenticate()

    assert user.id == user_id
    assert user.username == username


@pytest.mark.parametrize(
    'username, password',
    [
        ('wrong_username_1', 'wrong_root_pw'),
        ('wrong_username_2', 'wrong_user_pw'),
        ('wrong_username_3', 'wrong_user_pw'),
    ],
)
def test_credentials_authenticator_wrong_username(
    my_data: MyData, username: str, password: str
) -> None:
    """Test authenticating with a invalid credentials authenticator.

    Args:
        my_data: a instance of a MyData object.
        username: the username to test with.
        password: the password to test with.
    """
    credentials_authenticator = CredentialsAuthenticator(
        username=username, password=password, second_factor=None
    )
    user_authenticator = UserAuthenticator(
        my_data_object=my_data, authenticator=credentials_authenticator
    )

    with pytest.raises(AuthenticationFailedError):
        _ = user_authenticator.authenticate()


@pytest.mark.parametrize(
    'username, password',
    [
        ('root', 'wrong_root_pw'),
        ('normal.user.1', 'wrong_user_pw'),
        ('normal.user.2', 'wrong_user_pw'),
    ],
)
def test_credentials_authenticator_wrong_password(
    my_data: MyData, username: str, password: str
) -> None:
    """Test authenticating with a invalid password.

    Args:
        my_data: a instance of a MyData object.
        username: the username to test with.
        password: the password to test with.
    """
    credentials_authenticator = CredentialsAuthenticator(
        username=username, password=password, second_factor=None
    )
    user_authenticator = UserAuthenticator(
        my_data_object=my_data, authenticator=credentials_authenticator
    )

    with pytest.raises(AuthenticationFailedError):
        _ = user_authenticator.authenticate()


@pytest.mark.parametrize(
    'username, password', [('service_user', 'service_password')]
)
def test_credentials_authenticator_service_user(
    my_data: MyData, username: str, password: str
) -> None:
    """Test authenticating with a a service user.

    Args:
        my_data: a instance of a MyData object.
        username: the username to test with.
        password: the password to test with.
    """
    credentials_authenticator = CredentialsAuthenticator(
        username=username, password=password, second_factor=None
    )
    user_authenticator = UserAuthenticator(
        my_data_object=my_data, authenticator=credentials_authenticator
    )

    with pytest.raises(AuthenticationFailedError):
        _ = user_authenticator.authenticate()


def test_creating_api_token(my_data: MyData, normal_user_1: User) -> None:
    """Test creating a API token authenticator.

    Args:
        my_data: a instance of a MyData object.
        normal_user_1: a normal user to test with.
    """
    credentials_authenticator = CredentialsAuthenticator(
        username=normal_user_1.username,
        password='normal_user_1_pw',
        second_factor=None,
    )
    user_authenticator = UserAuthenticator(
        my_data_object=my_data, authenticator=credentials_authenticator
    )
    user_authenticator.create_api_token(
        session_timeout_in_seconds=3600, title='test'
    )

    with my_data.get_context(normal_user_1) as context:
        api_tokens = context.api_tokens.retrieve(APIToken.title == 'test')  # type: ignore
        assert len(api_tokens) == 1


def test_credentials_authenticating_with_invalid_authenticator() -> None:
    """Test authenticating with a invalid UserAuthenticator.

    Should raise an error.
    """
    authenticator = CredentialsAuthenticator(
        username='service_user', password='service_pass', second_factor=None
    )
    with pytest.raises(AuthenticatorNotConfiguredError):
        authenticator.authenticate()


def test_credentials_authenticator_valid_credentials_with_2fa(
    my_data: MyData, normal_user_2: User
) -> None:
    """Test authenticating with for a user without 2FA.

    Args:
        my_data: a instance of a MyData object.
        normal_user_2: a normal user to test with.
    """
    # Test authentication
    credentials_authenticator = CredentialsAuthenticator(
        username=normal_user_2.username,
        password='normal_user_2_pw',
        second_factor='123456',
    )
    user_authenticator = UserAuthenticator(
        my_data_object=my_data, authenticator=credentials_authenticator
    )
    with pytest.raises(AuthenticationFailedError):
        _ = user_authenticator.authenticate()
