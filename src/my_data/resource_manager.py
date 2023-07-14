"""Module with the ResourceManager class.

Contains the ResourceManager class that is used by a Context to create a
ResourceManager for specific resources.
"""
from typing import Generic, Type, TypeVar

from sqlalchemy.future import Engine
from sqlalchemy.sql.elements import ColumnElement

from .context_data import ContextData
from .creators import Creator, UserScopedCreator
from .deleters import Deleter, UserScopedDeleter
from .retrievers import Retriever, UserScopedRetriever
from .updaters import Updater, UserScopedUpdater

T = TypeVar('T')


class ResourceManager(Generic[T]):
    """Manager for resources in the database.

    The ResourceManager class is used to manage resources in the database in a
    CRUD way. This means that this class gets a Creator, Retriever, Updater and
    Deleter class assigned to create, retrieve, update and delete resources.

    Attributes:
        _database_model: the SQLmodel model used by this ResourceManager.
        _database_engine: the SQLalchemy engine to use.
        _context_data: specifies in what context to execute the methods.
        retriever: a instance of a subclass of Retriever. This retrieves the
            actual data.
        creator: a instance of a subclass of Creator. This creates the actual
            data.
        updater: a instance of a subclass of Updater. This updates the actual
            data.
        deleter: a instance of a subclass of Deleter. This deletes the actual
            data.
    """

    def __init__(self,
                 database_model: Type[T],
                 database_engine: Engine,
                 context_data: ContextData | None = None,
                 creator: Type = UserScopedCreator,
                 retriever: Type = UserScopedRetriever,
                 updater: Type = UserScopedUpdater,
                 deleter: Type = UserScopedDeleter) -> None:
        """Set attributes for the object.

        The initiator sets the attributes for the object.

        Args:
            database_model: the SQLmodel model used by this ResourceManager.
            database_engine: the SQLalchemy engine to use.
            context_data: specifies in what context to execute the methods.
            creator: the class for the Creator.
            retriever: the class for the Retriever.
            updater: the class for the Updater.
            deleter: the class for the Deleter.
        """
        self._database_model: Type = database_model
        self._database_engine: Engine = database_engine
        self._context_data: ContextData | None = context_data

        self.retriever: Retriever = retriever(
            database_model=database_model,
            database_engine=database_engine,
            context_data=context_data
        )
        self.creator: Creator = creator(
            database_model=database_model,
            database_engine=database_engine,
            context_data=context_data
        )
        self.updater: Updater = updater(
            database_model=database_model,
            database_engine=database_engine,
            context_data=context_data
        )
        self.deleter: Deleter = deleter(
            database_model=database_model,
            database_engine=database_engine,
            context_data=context_data
        )

    def create(self, models: list[T] | T) -> list[T]:
        """Create resources.

        Creates one or multiple resources. It uses the defined creator to
        create the resource in the correct way.

        Args:
            models: the model or models to add.

        Returns:
            Model: the new model.
        """
        return self.creator.create(models)

    def retrieve(
            self,
            flt: list[ColumnElement] | ColumnElement | None = None) -> list[T]:
        """Retrieve resources for the specified object.

        Returns a list of resources for the specified model. It does this using
        the defined retriever to make sure it partains to the specified
        ContextData-object.

        Args:
            flt: SQLModel type filters to filter this resource.

        Returns:
            list[Model]: a list with the retrieved resources in models defined
                in the `my-models` package.
        """
        # Get all DB objects from the database
        return self.retriever.retrieve(flt=flt)

    def update(self, models: list[T] | T) -> list[T]:
        """Update resources.

        Updates one ore more resources. It uses the defined Updater to update
        the resource in the correct way.

        Args:
            models: the model or models to update.

        Returns:
            Model: the updated model.
        """
        return self.updater.update(models)

    def delete(self, models: list[T] | T) -> None:
        """Delete resources.

        Deletes one or more resources. It uses the defined Deleter to delete
        the resource in the correct way.

        Args:
            models: the model or models to update.
        """
        self.deleter.delete(models)
