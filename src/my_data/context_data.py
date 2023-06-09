"""Module with the `ContextData` class.

This module contains the `ContextData` class that can be used to specify the
context-variables in which a `Context` object should operate.
"""
from pydantic.dataclasses import dataclass
from my_model.user import User  # type: ignore


@dataclass
class ContextData:
    """Class with ContextData.

    Dataclass that contains the data for a `Context`-object. The properties
    defined in this class define the context that is being used.

    Attributes:
        user: a user object representing this context.
    """

    user: User | None = None
