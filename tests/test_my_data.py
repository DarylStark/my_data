"""Tests for the MyData object."""

import pytest
from my_model.user_scoped_models import User

from my_data.exceptions import (DatabaseNotConfiguredException,  # type:ignore
                                PermissionDeniedException)
from my_data.my_data import MyData  # type:ignore


def test_creating_empty_engine() -> None:
    """Test creating a MyData object with a empty engine.

    Should result in a DatabaseNotConfiguredException error.
    """

    my_data = MyData()
    with pytest.raises(DatabaseNotConfiguredException):
        my_data.create_engine()


def test_creating_context_empty_engine(root_user: User) -> None:
    """Test creating a context without a engine.

    Args:
        root_user: a root user to test with.

    Should result in a DatabaseNotConfiguredException error.
    """
    my_data = MyData()
    with pytest.raises(DatabaseNotConfiguredException):
        _ = my_data.get_context(root_user)


def test_creating_svc_context_empty_engine(service_user: User) -> None:
    """Test creating a context without a engine.

    Args:
        service_user: a service user to test.

    Should result in a DatabaseNotConfiguredException error.
    """
    my_data = MyData()
    with pytest.raises(DatabaseNotConfiguredException):
        _ = my_data.get_context_for_service_user(
            username=service_user.username,
            password='test')


def test_creating_svc_context_wrong_svc_username(my_data: MyData) -> None:
    """Test creating a service context with a wrong username.

    Args:
        my_data: a configured MyData object.

    Should result in a PermissionDeniedException error.
    """
    with pytest.raises(PermissionDeniedException):
        _ = my_data.get_context_for_service_user(
            username='wrong_service_user',
            password='test')


def test_creating_svc_context_wrong_svc_password(my_data: MyData) -> None:
    """Test creating a service context with a wrong password.

    Args:
        my_data: a configured MyData object.

    Should result in a PermissionDeniedException error.
    """
    with pytest.raises(PermissionDeniedException):
        _ = my_data.get_context_for_service_user(
            username='service.user',
            password='test')