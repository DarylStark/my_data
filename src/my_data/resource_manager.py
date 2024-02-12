"""Module with the ResourceManager class.

Contains the ResourceManager class that is used by a Context to create a
ResourceManager for specific resources.
"""
import logging
from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from sqlalchemy.future import Engine
from sqlalchemy.sql.elements import ColumnElement

from my_model import MyModel

from .context_data import ContextData
from .creators import Creator, UserCreator, UserScopedCreator
from .deleters import Deleter, UserDeleter, UserScopedDeleter
from .retrievers import Retriever, UserRetriever, UserScopedRetriever
from .updaters import Updater, UserScopedUpdater, UserUpdater

T = TypeVar('T', bound=MyModel)


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
                 context_data: ContextData,
                 creator: Type[Creator[T]] = UserScopedCreator,
                 retriever: Type[Retriever[T]] = UserScopedRetriever,
                 updater: Type[Updater[T]] = UserScopedUpdater,
                 deleter: Type[Deleter[T]] = UserScopedDeleter) -> None:
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
        self._logger = logging.getLogger(f'ResourceManager-{id(self)}')
        self._logger.info('ResourceManager object created')
        self._database_model: Type[T] = database_model
        self._database_engine: Engine = database_engine
        self._context_data: ContextData = context_data

        self.retriever: Retriever[T] = retriever(
            database_model=database_model,
            database_engine=database_engine,
            context_data=context_data
        )
        self.creator: Creator[T] = creator(
            database_model=database_model,
            database_engine=database_engine,
            context_data=context_data
        )
        self.updater: Updater[T] = updater(
            database_model=database_model,
            database_engine=database_engine,
            context_data=context_data
        )
        self.deleter: Deleter[T] = deleter(
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
            flt: list[ColumnElement[bool]] | ColumnElement[bool] | None = None,
            sort: ColumnElement[T] | None = None,
            start: int | None = None,
            max_items: int | None = None) -> list[T]:
        """Retrieve resources for the specified object.

        Returns a list of resources for the specified model. It does this using
        the defined retriever to make sure it partains to the specified
        ContextData-object.

        Args:
            flt: SQLModel type filters to filter this resource.
            sort: the SQLmodel field to sort on.
            start: the index of the first item to retrieve.
            max_items: the maximum number of items to retrieve.

        Returns:
            list[Model]: a list with the retrieved resources in models defined
                in the `my-models` package.
        """
        # Get all DB objects from the database
        return self.retriever.retrieve(
            flt=flt,
            sort=sort,
            start=start,
            max_items=max_items)

    def count(
            self,
            flt: list[ColumnElement[bool]] | ColumnElement[bool] | None = None
    ) -> int:
        """Retrieve the number of records for a given query.

        Returns the count of records in the given query. This method can be
        used to retrieve the number of records in a query, without retrieving
        the actual records.

        Args:
            flt: SQLModel type filters to filter this resource.

        Returns:
            The number of records in the given query.
        """
        # Get the count of the DB objects
        return self.retriever.count(flt=flt)

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


class ResourceManagerFactory(Generic[T], ABC):
    """Factory for ResourceManagers.

    Abstract class for a factory that creates ResourceManagers.
    """

    def __init__(self,
                 database_model: Type[T],
                 database_engine: Engine,
                 context_data: ContextData) -> None:
        """Set attributes for the object.

        Args:
            database_model: the SQLmodel model used by this ResourceManager.
            database_engine: the SQLalchemy engine to use.
            context_data: specifies in what context to execute the methods.
        """
        self._database_model: Type[T] = database_model
        self._database_engine: Engine = database_engine
        self._context_data: ContextData = context_data

    def create(self) -> ResourceManager[T]:
        """Create a ResourceManager.

        Returns:
            ResourceManager: the created ResourceManager.
        """
        return ResourceManager(
            database_model=self._database_model,
            database_engine=self._database_engine,
            context_data=self._context_data,
            creator=self._create_creator(),
            retriever=self._create_retriever(),
            updater=self._create_updater(),
            deleter=self._create_deleter()
        )

    @abstractmethod
    def _create_creator(self) -> Type[Creator[T]]:
        """Create a Creator.

        Returns:
            Creator: the created Creator.
        """

    @abstractmethod
    def _create_retriever(self) -> Type[Retriever[T]]:
        """Create a Retriever.

        Returns:
            Retriever: the created Retriever.
        """

    @abstractmethod
    def _create_updater(self) -> Type[Updater[T]]:
        """Create a Updater.

        Returns:
            Updater: the created Updater.
        """

    @abstractmethod
    def _create_deleter(self) -> Type[Deleter[T]]:
        """Create a Deleter.

        Returns:
            Deleter: the created Deleter.
        """


class UserResourceManagerFactory(ResourceManagerFactory[T]):
    """Factory for ResourceManagers for User resources.

    The UserResourceManagerFactory is a factory that creates ResourceManagers
    for User resources.
    """

    def _create_creator(self) -> Type[Creator[T]]:
        """Create a Creator.

        Returns:
            Creator: the created Creator.
        """
        return UserCreator[T]

    def _create_retriever(self) -> Type[Retriever[T]]:
        """Create a Retriever.

        Returns:
            Retriever: the created Retriever.
        """
        return UserRetriever[T]

    def _create_updater(self) -> Type[Updater[T]]:
        """Create a Updater.

        Returns:
            Updater: the created Updater.
        """
        return UserUpdater[T]

    def _create_deleter(self) -> Type[Deleter[T]]:
        """Create a Deleter.

        Returns:
            Deleter: the created Deleter.
        """
        return UserDeleter[T]


class UserScopedResourceManagerFactory(ResourceManagerFactory[T]):
    """Factory for ResourceManagers for UserScoped resources.

    The UserResourceManagerFactory is a factory that creates ResourceManagers
    for UserScoped resources.
    """

    def _create_creator(self) -> Type[Creator[T]]:
        """Create a Creator.

        Returns:
            Creator: the created Creator.
        """
        return UserScopedCreator[T]

    def _create_retriever(self) -> Type[Retriever[T]]:
        """Create a Retriever.

        Returns:
            Retriever: the created Retriever.
        """
        return UserScopedRetriever[T]

    def _create_updater(self) -> Type[Updater[T]]:
        """Create a Updater.

        Returns:
            Updater: the created Updater.
        """
        return UserScopedUpdater[T]

    def _create_deleter(self) -> Type[Deleter[T]]:
        """Create a Deleter.

        Returns:
            Deleter: the created Deleter.
        """
        return UserScopedDeleter[T]
