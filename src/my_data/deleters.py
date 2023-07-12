"""TODO: documentation."""

from typing import Type

from .data_manipulator import DataManipulator


class Deleter(DataManipulator):
    """TODO: documentation."""

    def delete(self, models: list | Type) -> list:
        pass


class UserScopedDeleter(Deleter):
    """TODO: documentation."""


class UserDeleter(Deleter):
    """TODO: documentation."""
