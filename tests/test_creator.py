"""Module with tests for the Creator classes."""

import pytest
from my_model.user_scoped_models import Tag, User

from my_data.context_data import ContextData
from my_data.creators import Creator, UserCreator, UserScopedCreator
from my_data.exceptions import (BaseClassCallException,
                                WrongDataManipulatorException)
from my_data.my_data import MyData


def test_base_class_exception(my_data: MyData, root_user: User) -> None:
    """Test if we get an exception when starting a pure virtual method.

    Should raise a BaseClassCallException.

    Args:
        my_data: a instance of a MyData object.
        root_user: a root user to test.
    """
    if my_data.database_engine:
        creator = Creator(
            database_model=User,
            database_engine=my_data.database_engine,
            context_data=ContextData(my_data.database_engine, user=root_user))
        with pytest.raises(BaseClassCallException):
            creator.is_authorized()
    else:
        assert TypeError, "MyData not configured"


def test_userscoped_wrong_manipulator_exception(
        my_data: MyData, root_user: User) -> None:
    """Test if we get an exception when using a wrong model.

    Should raise a WrongDataManipulatorException.

    Args:
        my_data: a instance of a MyData object.
        root_user: a root user to test.
    """
    if my_data.database_engine:
        creator = UserScopedCreator(
            database_model=User,
            database_engine=my_data.database_engine,
            context_data=ContextData(my_data.database_engine, user=root_user))
        with pytest.raises(WrongDataManipulatorException):
            creator.is_authorized()
    else:
        assert TypeError, "MyData not configured"


def test_usercreator_wrong_manipulator_exception(
        my_data: MyData, root_user: User) -> None:
    """Test if we get an exception when using a wrong model.

    Should raise a WrongDataManipulatorException.

    Args:
        my_data: a instance of a MyData object.
        root_user: a root user to test.
    """
    if my_data.database_engine:
        creator = UserCreator(
            database_model=Tag,
            database_engine=my_data.database_engine,
            context_data=ContextData(my_data.database_engine, user=root_user))
        with pytest.raises(WrongDataManipulatorException):
            creator.is_authorized()
    else:
        assert TypeError, "MyData not configured"
