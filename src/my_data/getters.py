"""The Getters for the ResourceManager.

This module contains the Getters for the ResourceManager. It contains the
base-class and the subclasses.
"""
from my_model.user import UserRole  # type: ignore
from sqlalchemy.sql.elements import ColumnElement
from sqlmodel import SQLModel, select

from .crud_base import CRUDBase
from .db_connection import db_connection
from .db_models import DBUser


class Getter(CRUDBase):
    """Base Getter class.

    The base Getter class should be used as the base class for specific
    Getter-classes. The base class defines the interface for all
    Getter-classes.
    """

    def filters(self) -> list[ColumnElement]:
        """Get the specific filters for this Getter.

        Returns the specific filters for this getter. These filters define
        which resources are retrieved, using the ContextData-object.

        Raises:
            NotImplementedError: raised when this method is used for the base
                class instead of a subclass.
        """
        raise NotImplementedError('Filters are not implemented for this type')

    def get(self) -> list[SQLModel]:
        """Get the resources.

        Get the resources for the specified DB object within the context of the
        given ContextData object.

        Returns:
            list[SQLModel]: a list with the resources.
        """
        with db_connection.get_session() as session:
            resources = select(self._db_model)
            for flt in self.filters():
                resources = resources.where(flt)
            results = session.exec(resources)
            return list(results)


class UserSpecificGetter(Getter):
    """Getter for user specific resources.

    This getter should be used for resources that are bound to specific users,
    like tags and API tokens.
    """

    def filters(self) -> list[ColumnElement]:
        """Get the specific filters for this getter.

        For this specific getter it filters on the user_id field of the object.

        Returns:
            list[ColumnElement]: a list with SQLalchemy filters.
        """
        filters: list[ColumnElement] = []
        if self._context_data.user:
            filters.append(
                self._db_model.user_id == self._context_data.user.id)
        return filters


class UserGetter(Getter):
    """Getter for user resources.

    This getter should be used for User resources. These resources are not
    bound to a specific user but depend on the role a user has.
    """

    def filters(self) -> list[ColumnElement]:
        """Get the specific filters for this getter.

        For this specific getter it filters on the user_role field of the user
        object. This only happens when the User object in the ContextData
        object is a normal user. Root users can retrieve _all_ users, normal
        users can only retrieve their own account.

        Returns:
            list[ColumnElement]: a list with SQLalchemy filters.
        """
        filters: list[ColumnElement] = []
        if self._context_data.user:
            if self._context_data.user.role == UserRole.USER:
                filters.append(
                    DBUser.id == self._context_data.user.id
                )
        return filters
