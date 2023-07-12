"""TODO: documentation."""

from typing import Type

from .data_manipulator import DataManipulator


class Updater(DataManipulator):
    """TODO: documentation."""

    def update(self, models: list | Type) -> list:
        pass


class UserScopedUpdater(Updater):
    """TODO: documentation."""


class UserUpdater(Updater):
    """TODO: documentation."""
