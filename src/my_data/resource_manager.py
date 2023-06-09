"""Module for ResourceManagers.

This module contains the ResourceManager class and classes for Getters. The
Getters are used to retrieve data using the specified ContextData-objects.
"""
from typing import Type

from my_model._model import Model  # type: ignore

from .context_data import ContextData
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
