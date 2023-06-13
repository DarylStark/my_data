"""The Getters for the ResourceManager.

This module contains the Getters for the ResourceManager. It contains the
base-class and the subclasses.
"""
from my_model._model import Model  # type: ignore
from my_model.user import UserRole  # type: ignore
from sqlalchemy.sql.elements import ColumnElement
from sqlmodel import select

from .crud_base import CRUDBase
from .db_connection import db_connection
from .db_models import DBUser
from .exceptions import InvalidFilterFieldException


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

    def get(self,
            raw_filters: list[ColumnElement] | None = None,
            **kwargs: dict) -> list[Model]:
        """Get the resources.

        Get the resources for the specified DB object within the context of the
        given ContextData object.

        Args:
            raw_filters: raw SQLModel type filters to filter this resource.
            **kwargs: named filers.

        Returns:
            list[Model]: a list with the resources in `my-model` format.

        Raises:
            InvalidFilterFieldException: when a invalid named filter is used.
        """
        with db_connection.get_session() as session:
            resources = select(self._db_model)

            # Filter on the default filters for this object.
            for flt in self.filters():
                resources = resources.where(flt)

            # Set the extra 'raw' filters from the arguments
            if raw_filters:
                for flt in raw_filters:
                    resources = resources.where(flt)

            # Add the fiilters that were given via named arguments
            for field, value in kwargs.items():
                if not hasattr(self._db_model, field):
                    raise InvalidFilterFieldException(
                        f'The model "{self._db_model}" has no field "{field}"')
                resources = resources.where(
                    getattr(self._db_model, field) == value
                )

            # Execute the query
            results = session.exec(resources)

            # Convert them to the correct model
            new_resources: list[Model] = [
                self._model(**x.dict())
                for x in results
            ]

        return new_resources


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
