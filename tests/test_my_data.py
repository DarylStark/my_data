"""Tests for the MyData object."""

import pytest
from my_data.exceptions import DatabaseNotConfiguredError
from my_data.my_data import MyData
from my_model import User


def test_creating_empty_engine() -> None:
    """Test creating a MyData object with a empty engine.

    Should result in a DatabaseNotConfiguredException error.
    """
    my_data = MyData()
    with pytest.raises(DatabaseNotConfiguredError):
        my_data.create_engine()


def test_creating_context_empty_engine(root_user: User) -> None:
    """Test creating a context without a engine.

    Args:
        root_user: a root user to test with.

    Should result in a DatabaseNotConfiguredException error.
    """
    my_data = MyData()
    with pytest.raises(DatabaseNotConfiguredError):
        _ = my_data.get_context(root_user)


def test_creating_svc_context_empty_engine() -> None:
    """Test creating a context without a engine.

    Should result in a DatabaseNotConfiguredException error.
    """
    my_data = MyData()
    with pytest.raises(DatabaseNotConfiguredError):
        _ = my_data.get_context_for_service_user()
