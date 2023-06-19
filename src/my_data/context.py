"""Module with the `Context` class.

This module contains the `Context` class which can be used, in combination with
a `ContextData` object, to specify a specific context.
"""
from types import TracebackType

from my_model.tag import Tag  # type: ignore
from my_model.user import User  # type: ignore

from .context_data import ContextData
from .getters import UserGetter
from .creators import UserCreator
from .resource_manager import ResourceManager
from .updaters import UserUpdater
from .deleters import UserDeleter


class Context:
    """Class to manage resources within a `Context`.

    This class can be used in combination with a `ContextData` class to create
    a context in which resources are managed. Resources are managed with
    `ResourceManager` objects; for each resource, one `ResourceManager` object
    if created.

    Attributes:
        context_data: the context data for this `Context`
        tags: a resource manager for tags
        users: a resource manager for users
    """

    def __init__(self,
                 user: User | None = None) -> None:
        """Create a Context.

        To create a context, specify the contextdata options als parameters for
        this object.

        Args:
            user: the user object in which this context exists.
        """
        # Object with the context data in it
        self.context_data = ContextData(user=user)

        # Objects to manage data objects
        self.tags = ResourceManager(db_model=Tag,
                                    context_data=self.context_data)

        self.users = ResourceManager(db_model=User,
                                     context_data=self.context_data,
                                     getter=UserGetter,
                                     creator=UserCreator,
                                     updater=UserUpdater,
                                     deleter=UserDeleter)

    def __enter__(self) -> 'Context':
        """Start method for a Pythonic context manager.

        Starts the context manager.

        Returns:
            Context: returns the instance of itself
        """
        return self

    def __exit__(self,
                 exception_type: BaseException | None,
                 exception_value: BaseException | None,
                 traceback: TracebackType | None) -> bool:
        """End method of the Pythonic context manager.

        Runs when the context manager is done. If this returns True, the
        context manager is considered to be successful. If it returns False,
        the context manager is considered to be unsuccessful.

        Args:
            exception_type: the type of exception that occured
            exception_value: the value of the exception that occured
            traceback: the traceback for the exception that occured

        Returns:
            bool: True when everything was fine, False when there was a
                unhandled exception.
        """
        return exception_type is None
