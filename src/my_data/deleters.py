"""The deleters for the ResourceManager.

This module contains the Deleters for the ResourceManager. It contains the
base-class and the subclasses.
"""

from my_model.model import Model  # type: ignore
from my_model.user import UserRole  # type: ignore
from sqlmodel import SQLModel

from my_data.db_connection import db_connection
from my_data.exceptions import PermissionDeniedException

from .crud_base import CRUDBase
from .exceptions import InvalidModelException


class Deleter(CRUDBase):
    """Base Deleter class.

    TODO: Fill in
    """

    def delete(self, models: list[Model] | Model) -> None:
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
