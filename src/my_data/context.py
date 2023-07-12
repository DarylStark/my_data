"""TODO: documentation."""
from types import TracebackType

from my_model.user_scoped_models import Tag, User
from sqlalchemy.future import Engine

from my_data.creators import UserCreator, UserScopedCreator
from my_data.deleters import UserDeleter, UserScopedDeleter
from my_data.resource_manager import ResourceManager
from my_data.retrievers import UserRetriever, UserScopedRetriever
from my_data.updaters import UserScopedUpdater, UserUpdater

from .context_data import ContextData


class Context:
    """TODO: documentation."""

    def __init__(self,
                 database_engine: Engine,
                 context_data: ContextData) -> None:
        """TODO: documentation."""
        self.database_engine = database_engine
        self._context_data = context_data

        # Exposure of Resource Managers to manage specific resources in the
        # data model.
        self.users = ResourceManager(
            database_model=User,
            database_engine=database_engine,
            context_data=self._context_data,
            creator=UserCreator,
            retriever=UserRetriever,
            updater=UserUpdater,
            deleter=UserDeleter)
        self.tags = ResourceManager(
            database_model=Tag,
            database_engine=database_engine,
            context_data=self._context_data,
            creator=UserScopedCreator,
            retriever=UserScopedRetriever,
            updater=UserScopedUpdater,
            deleter=UserScopedDeleter)

    def __enter__(self) -> 'Context':
        """TODO: documentation."""
        return self

    def __exit__(self,
                 exception_type: BaseException | None,
                 exception_value: BaseException | None,
                 traceback: TracebackType | None) -> bool:
        """TODO: documentation."""
        return exception_type is None
