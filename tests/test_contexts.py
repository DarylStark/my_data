"""Unit tests for Context objects."""

import pytest
from my_model.user_scoped_models import User

from my_data import MyData
from my_data.exceptions import PermissionDeniedException


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


def test_creating_service_context_with_normal_account(
        my_data: MyData,
        normal_user_1: User) -> None:
    """Test creating a service context with a normal account.

    Should result in a PermissionDeniedException exception.

    Args:
        my_data: the MyData object to test with.
        normal_user_1: a normal user to test with.
    """
    with pytest.raises(PermissionDeniedException):
        with my_data.get_context_for_service_user(
                username=normal_user_1.username,
                password='normal_user_1_pw'):
            ...
