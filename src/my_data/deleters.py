"""The deleters for the ResourceManager.

This module contains the Deleters for the ResourceManager. It contains the
base-class and the subclasses.
"""

from sqlmodel import SQLModel

from .crud_base import CRUDBase


class Deleter(CRUDBase):
    """Base Deleter class.

    TODO: Fill in
    """

    def delete(self, models: list[SQLModel] | SQLModel) -> None:
        """Delete the model from the database.

        TODO: Fill in
        """


class UserSpecificDeleter(Deleter):
    """Deleter for user specific resources.

    TODO: Fill in
    """


class UserDeleter(Deleter):
    """Deleter for user resources.

    TODO: Fill in
    """
