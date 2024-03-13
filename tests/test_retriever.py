"""Module with tests for the Retriever classes."""

import pytest
from my_data.context_data import ContextData
from my_data.exceptions import (
    BaseClassCallError,
    WrongDataManipulatorError,
)
from my_data.my_data import MyData
from my_data.retrievers import Retriever, UserRetriever, UserScopedRetriever
from my_model import Tag, User


def test_base_class_exception(my_data: MyData, root_user: User) -> None:
    """Test if we get an exception when starting a pure virtual method.

    Should raise a BaseClassCallException.

    Args:
        my_data: a instance of a MyData object.
        root_user: a root user to test.
    """
    if my_data.database_engine:
        retriever = Retriever(
            database_model=User,
            database_engine=my_data.database_engine,
            context_data=ContextData(my_data.database_engine, user=root_user),
        )
        with pytest.raises(BaseClassCallError):
            retriever.get_context_filters()
    else:
        raise AssertionError()


def test_userscoped_wrong_manipulator_exception(
    my_data: MyData, root_user: User
) -> None:
    """Test if we get an exception when using a wrong model.

    Should raise a WrongDataManipulatorException.

    Args:
        my_data: a instance of a MyData object.
        root_user: a root user to test.
    """
    if my_data.database_engine:
        creator = UserScopedRetriever(
            database_model=User,
            database_engine=my_data.database_engine,
            context_data=ContextData(my_data.database_engine, user=root_user),
        )
        with pytest.raises(WrongDataManipulatorError):
            creator.get_context_filters()
    else:
        raise AssertionError()


def test_usercreator_wrong_manipulator_exception(
    my_data: MyData, root_user: User
) -> None:
    """Test if we get an exception when using a wrong model.

    Should raise a WrongDataManipulatorException.

    Args:
        my_data: a instance of a MyData object.
        root_user: a root user to test.
    """
    if my_data.database_engine:
        creator = UserRetriever(
            database_model=Tag,
            database_engine=my_data.database_engine,
            context_data=ContextData(my_data.database_engine, user=root_user),
        )
        with pytest.raises(WrongDataManipulatorError):
            creator.get_context_filters()
    else:
        raise AssertionError()
