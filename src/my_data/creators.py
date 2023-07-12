"""TODO: documentation."""

from typing import Type

from .data_manipulator import DataManipulator


class Creator(DataManipulator):
    """TODO: documentation."""

    def create(self, models: list | Type) -> list:
        pass


class UserScopedCreator(Creator):
    """TODO: documentation."""


class UserCreator(Creator):
    """TODO: documentation."""
