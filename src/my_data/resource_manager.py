"""Module for ResourceManagers.

This module contains the ResourceManager class and classes for Getters. The
Getters are used to retrieve data using the specified ContextData-objects.
"""
from typing import Type

from my_model._model import Model  # type: ignore
from sqlalchemy.sql.elements import ColumnElement

from .context_data import ContextData
from .creators import Creator, UserSpecificCreator
from .getters import Getter, UserSpecificGetter


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
                 getter: Type = UserSpecificGetter,
                 creator: Type = UserSpecificCreator) -> None:
        """Manage database resources.

        Should be used by a `Context` to manage specific resources.

        Args:
            model: the `my-model` model for the resources.
            db_model: the DB model for the resources.
            context_data: the context data in which the resources should be
                managed.
            getter: a instance of a Getter that retrives the data.
            creator: a instance of Creator that creates the data.
        """
        self._model: Type = model
        self._db_model: Type = db_model
        self._context_data: ContextData | None = context_data

        self.getter: Getter = getter(
            context_data=self._context_data,
            model=self._model,
            db_model=self._db_model)
        self.creator: Creator = creator(
            context_data=self._context_data,
            model=self._model,
            db_model=self._db_model)

    def get(self,
            raw_filters: list[ColumnElement] | None = None,
            **kwargs: dict) -> list[Model]:
        """Get all resources for the specified object.

        Returns a list of resources for the specified model. It does this using
        the defined getter to make sure it partains to the specified
        ContextData-object.

        Args:
            raw_filters: raw SQLModel type filters to filter this resource.

        Returns:
            list[Model]: a list with the retrieved resources in models defined
                in the `my-models` package.
        """
        # Get all DB objects from the database
        return self.getter.get(raw_filters=raw_filters, **kwargs)

    def create(self, models: list[Model] | Model) -> None:
        """Create resources.

        Creates one or multiple resources. It uses the defined creator to
        create the resource in the correct way.

        Args:
            models: the model or models to add
        """
        self.creator.create(models)
