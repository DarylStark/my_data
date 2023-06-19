"""The updaters for the ResourceMAaager.

This module contains the Updaters for the ResourceManager. It contains the
base-class and the subclasses.
"""

from my_model.model import Model  # type: ignore
from my_model.user import UserRole  # type: ignore
from sqlmodel import SQLModel

from my_data.db_connection import db_connection

from .crud_base import CRUDBase
from .exceptions import InvalidModelException, PermissionDeniedException


class Updater(CRUDBase):
    """Base Updater class.

    TODO: Fill in
    """

    def update(self, models: list[Model] | Model) -> list[Model]:
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
