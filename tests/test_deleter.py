"""Module with tests for the Deleter classes."""

import pytest
from my_model.user_scoped_models import Tag, User

from my_data.context_data import ContextData  # type:ignore
from my_data.deleters import UserDeleter  # type:ignore
from my_data.exceptions import WrongDataManipulatorException  # type:ignore
from my_data.my_data import MyData  # type:ignore


def test_usercreator_wrong_manipulator_exception(
        my_data: MyData, root_user: User) -> None:
    """Test if we get an exception when using a wrong model.

    Should raise a WrongDataManipulatorException.

    Args:
        my_data: a instance of a MyData object.
        root_user: a root user to test.
    """
    if my_data.database_engine:
        deleter = UserDeleter(
            database_model=Tag,
            database_engine=my_data.database_engine,
            context_data=ContextData(my_data.database_engine, user=root_user))
        with pytest.raises(WrongDataManipulatorException):
            deleter.delete(Tag(title='test'))
    else:
        assert False, "MyData not configured"
