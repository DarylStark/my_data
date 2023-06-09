"""Module for ResourceManagers.

This module contains the ResourceManager class and classes for Getters. The
Getters are used to retrieve data using the specified ContextData-objects.
"""
from typing import Type

from my_model._model import Model  # type: ignore
from my_model.user import UserRole  # type: ignore
from sqlalchemy.sql.elements import ColumnElement
from sqlmodel import SQLModel, select

from my_data.context_data import ContextData

from .db_connection import db_connection
from .db_models import DBUser


class Getter:
    """Base Getter class.

    The base Getter class should be used as the base class for specific
    Getter-classes. The base class defines the interface for all
    Getter-classes.

    Attributes:
        _context_data: the passed ContextData object.
        _db_model: the database model that should be used to retrieve data.
    """

    def __init__(self, context_data: ContextData, db_model: Type) -> None:
        """Set the specifics for the Getter.

        To create the Getter, a ContextData object is required, and the DB
        model that is used to select data.

        Args:
            context_data: the `ContextData` object for this Getter.
            db_model: the DB Model for the object.
        """
        self._context_data = context_data
        self._db_model = db_model

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
    """Getter for user resources."""

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


class ResourceManager:
    """Manages resources in the database.

    A resource manager manages resources in the database. It does this by
    setting the needed my-model models and the DB models defined in this
    package (in the `db_models` module). It contains a instance of a
    Getter class that is configurable. This way, the data that is retrieved can
    be filtered in the correct way.

    Attributes:
        getter: a instance of a Getter that retrives the data.

        _model: the `my-model` model for the resources.
        _db_model: the DB model for the resources.
        _context_data: the context data in which the resources should be
            managed.
    """

    def __init__(self,
                 model: Type,
                 db_model: Type,
                 context_data: ContextData | None = None,
                 getter=UserSpecificGetter) -> None:
        """Manage database resources.

        Should be used by a `Context` to manage specific resources.

        Args:
            model: the `my-model` model for the resources.
            db_model: the DB model for the resources.
            context_data: the context data in which the resources should be
                managed.
            getter: a instance of a Getter that retrives the data.
        """
        self._model: Type = model
        self._db_model: Type = db_model
        self._context_data: ContextData | None = context_data

        self.getter: Getter = getter(
            context_data=self._context_data,
            db_model=self._db_model)

    def get(self) -> list[Model]:
        """Get all resources for the specified object.

        Returns a list of resources for the specified model. It does this using
        the defined getter to make sure it partains to the specified
        ContextData-object.

        Returns:
            list[Model]: a list with the retrieved resources in models defined
                in the `my-models` package.
        """
        # Get all DB objects from the database
        resources = self.getter.get()

        # Convert the resources to 'my_model' models
        new_resources: list[Model] = [
            self._model(**x.dict())
            for x in resources
        ]

        return new_resources
