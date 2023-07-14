"""Module with Creators.

This module contains the creator classes. These classes are used to create data
in the database. The ResourceManager uses these classes.
"""
from typing import TypeVar
from typing import Type

from .data_manipulator import DataManipulator

T = TypeVar('T')


class Creator(DataManipulator):
    """Baseclass for Creators.

    The baseclass for creators. The sub creators use this class to make sure
    creators have the same interface."""

    def create(self, models: list[T] | T) -> list[T]:
        """Create data.

        The method to create data in the database.

        Args:
            models: the models to create

        Returns:
            A list with the created data models.
        """


class UserScopedCreator(Creator):
    """Creator for UserScoped models.

    This creator should be used for UserScoped models, like Tags and APItokens.
    """


class UserCreator(Creator):
    """Creator for Users.

    This creator should be used to create Users.
    """
