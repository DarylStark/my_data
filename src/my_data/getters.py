"""The Getters for the ResourceManager.

This module contains the Getters for the ResourceManager. It contains the
base-class and the subclasses.
"""
from my_model.model import Model  # type: ignore
from my_model.user import User, UserRole  # type: ignore
from sqlalchemy.sql.elements import ColumnElement
from sqlmodel import select

from .crud_base import CRUDBase
from .db_connection import db_connection
from .exceptions import InvalidFilterFieldException


class Getter(CRUDBase):
    """Base Getter class.

    TODO: Fill in
    """

    def get(self,
            raw_filters: list[ColumnElement] | None = None,
            **kwargs: dict) -> list[Model]:
        """Get the resources.

        TODO: Fill in
        """


class UserSpecificGetter(Getter):
    """Getter for user specific resources.

    TODO: Fill in
    """


class UserGetter(Getter):
    """Getter for user resources.

    TODO: Fill in
    """
