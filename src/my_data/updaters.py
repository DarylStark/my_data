"""The updaters for the ResourceMAaager.

This module contains the Updaters for the ResourceManager. It contains the
base-class and the subclasses.
"""

from sqlmodel import SQLModel

from .crud_base import CRUDBase


class Updater(CRUDBase):
    """Base Updater class.

    TODO: Fill in
    """

    def update(self, models: list[SQLModel] | SQLModel) -> list[SQLModel]:
        """Update the model in the database.

        TODO: Fill in
        """


class UserSpecificUpdater(Updater):
    """Updater for user specific resources.

    TODO: Fill in
    """


class UserUpdater(Updater):
    """Updater for user resources.

    TODO: Fill in
    """
