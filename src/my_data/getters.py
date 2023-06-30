"""The Getters for the ResourceManager.

This module contains the Getters for the ResourceManager. It contains the
base-class and the subclasses.
"""
from my_model.user_scoped_models import User, UserRole  # type: ignore
from sqlalchemy.sql.elements import ColumnElement
from sqlmodel import SQLModel, select

from .crud_base import CRUDBase
from .db_connection import db_connection
from .exceptions import PermissionDeniedException


class Getter(CRUDBase):
    """Base Getter class.

    TODO: Fill in
    """

    def get_default_filters(self) -> list[ColumnElement]:
        """Default filters for the object.

        TODO: Fill in
        """
        return []

    def get(self,
            flt: list[ColumnElement] | None = None) -> list[SQLModel]:
        """Get the resources from the database.

        Gets the resources from the database and returns them. The client can
        give additional SQLmodel filters to filter the resources. By default,
        the filters from the subclass get used.

        # TODO: Fill in
        """

        # Check if the user is allowed to retrieve these resources
        if not self.is_authorized():
            raise PermissionDeniedException(
                'User is not authorized to retrieve this resource')

        # Retrieve the resources
        with db_connection.get_session() as session:
            sql_query = select(self._db_model)

            # ADd the default filters
            for filter_item in self.get_default_filters():
                sql_query = sql_query.where(filter_item)

            # Add the filters from the command line
            if flt:
                for filter_item in flt:
                    sql_query = sql_query.where(filter_item)

            resources = session.exec(sql_query).all()

        # Return the given resources
        return resources


class UserSpecificGetter(Getter):
    """Getter for user specific resources.

    TODO: Fill in
    """

    def is_authorized(self) -> bool:
        """Check if the current context can retrieve these objects.

        Checks whether the current context is allowed to retrieve these
        specific resources. It only checks if there is a user configured in the
        Context. If there isn't, it returns False. If there is, it returns
        True.

        Returns:
            bool: True if the user is allowed to retrieve resources from this
                type. False if the user is not allowed to do this.
        """
        return self._context_data.user is not None

    def get_default_filters(self) -> list[ColumnElement]:
        """Give the default filters for this resource.

        TODO: fill in
        """
        return [self._db_model.user_id == self._context_data.user.id]


class UserGetter(Getter):
    """Getter for user resources.

    TODO: Fill in
    """

    def is_authorized(self) -> bool:
        return (self._context_data.user is not None and
                self._db_model is User)

    def get_default_filters(self) -> list[ColumnElement]:
        """Give the default filters for this resource.

        TODO: fill in
        """
        if self._context_data.user.role == UserRole.USER:
            return [User.id == self._context_data.user.id]
        return []
