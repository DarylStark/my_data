"""Unit tests for Context objects."""

import pytest
from my_model import User

from my_data import MyData
from my_data.exceptions import PermissionDeniedException, ServiceUserNotConfiguredException, DatabaseNotConfiguredException


def test_creating_user_context_with_service_account(
        my_data: MyData,
        service_user: User) -> None:
    """Test creating a user context with a service account.

    Should result in a PermissionDeniedException exception.

    Args:
        my_data: the MyData object to test with.
        service_user: a service user to test with.
    """
    with pytest.raises(PermissionDeniedException):
        with my_data.get_context(user=service_user):
            ...


def test_creating_a_service_context_no_credentials(
        my_data: MyData) -> None:
    """Test creating a service context without service credentials.

    Should result in a ServiceUserNotConfiguredException exception.

    Args:
        my_data: the MyData object to test with.
    """
    old_service_username = my_data._service_username
    my_data._service_username = None
    with pytest.raises(ServiceUserNotConfiguredException):
        _ = my_data.get_context_for_service_user()
    my_data._service_username = old_service_username


def test_creating_a_service_context_wrong_username(
        my_data: MyData) -> None:
    """Test creating a service context with a wrong username.

    Should result in a PermissionDeniedException exception.

    Args:
        my_data: the MyData object to test with.
    """
    old_service_username = my_data._service_username
    old_service_account = my_data._service_user_account

    my_data._service_user_account = None
    my_data._service_username = 'wrong_username'

    with pytest.raises(PermissionDeniedException):
        _ = my_data.get_context_for_service_user()

    my_data._service_username = old_service_username
    my_data._service_user_account = old_service_account


def test_creating_a_service_context_wrong_password(
        my_data: MyData) -> None:
    """Test creating a service context with a wrong password.

    Should result in a PermissionDeniedException exception.

    Args:
        my_data: the MyData object to test with.
    """
    old_service_password = my_data._service_password
    old_service_account = my_data._service_user_account

    my_data._service_password = 'wrong_password'
    my_data._service_user_account = None

    with pytest.raises(PermissionDeniedException):
        _ = my_data.get_context_for_service_user()

    my_data._service_password = old_service_password
    my_data._service_user_account = old_service_account
