"""TODO: documentation. """
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
    """TODO: documentation. """

    def __init__(self,
                 database_model: Type[T],
                 database_engine: Engine,
                 context_data: ContextData | None = None,
                 creator: Type = UserScopedCreator,
                 retriever: Type = UserScopedRetriever,
                 updater: Type = UserScopedUpdater,
                 deleter: Type = UserScopedDeleter) -> None:
        """TODO: documentation. """
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

    def retrieve(self,
                 flt: list[ColumnElement] | None = None) -> list[T]:
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
