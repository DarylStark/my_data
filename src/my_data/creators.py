"""The creators for the ResourceManager.

This module contains the Creators for the ResourceManager. It contains the
base-class and the subclasses.
"""
from my_model.user_scoped_models import User  # type: ignore
from sqlmodel import SQLModel

from .crud_base import CRUDBase


class Creator(CRUDBase):
    """Base Creator class.

    TODO: Fill in
    """

    def create(self, models: SQLModel | list[SQLModel]) -> list[SQLModel]:
        """Create the data.

        TODO: Fill in
        """


class UserSpecificCreator(Creator):
    """Creator for user specific resources.

    TODO: Fill in
    """


class UserCreator(Creator):
    """Creator for user resources.

    This creator should be used to create users.
    """

    def get_updated_model(self, data: User) -> User:
        """Convert the User model to a User.

        TODO: Fill in
        """
