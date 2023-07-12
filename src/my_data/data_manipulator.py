"""TODO: documentation."""

from typing import Type, TypeVar, Generic
from .context_data import ContextData

from sqlalchemy.future import Engine

T = TypeVar('T')


class DataManipulator(Generic[T]):
    """TODO: documentation."""

    def __init__(self,
                 database_model: Type[T],
                 database_engine: Engine,
                 context_data: ContextData) -> None:
        """TODO: documentation."""
        self._database_model = database_model
        self._database_engine = database_engine
        self._context_data = context_data
