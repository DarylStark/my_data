"""Module with Creators.

This module contains the creator classes. These classes are used to create data
in the database. The ResourceManager uses these classes.
"""
from typing import TypeVar

from sqlmodel import Session

from .data_manipulator import DataManipulator
from .exceptions import BaseClassCallException, PermissionDeniedException

T = TypeVar('T')


class Creator(DataManipulator):
    """Baseclass for Creators.

    The baseclass for creators. The sub creators use this class to make sure
    creators have the same interface."""

    def is_authorized(self) -> bool:
        """Authorize the creation of this data.

        Method that checks if the current context is allowd to create this type
        of model.

        Raises:
            BaseClassCallException: BaseClass method is used.
        """
        raise BaseClassCallException('Method not implemented in baseclass')

    def create(self, models: list[T] | T) -> list[T]:
        """Create data.

        The method to create data in the database.

        Args:
            models: the models to create

        Returns:
            A list with the created data models.
        """

        if not self.is_authorized():
            raise PermissionDeniedException(
                'Not allowed to create this kind of object within the ' +
                'set context.')

        with Session(self._database_engine) as session:
            pass


class UserScopedCreator(Creator):
    """Creator for UserScoped models.

    This creator should be used for UserScoped models, like Tags and APItokens.
    """

    def is_authorized(self) -> bool:
        return False


class UserCreator(Creator):
    """Creator for Users.

    This creator should be used to create Users.
    """

    def is_authorized(self) -> bool:
        return False
