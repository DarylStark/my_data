"""Module with the DataManipulator class.

This module contains the DataManipulator class. This class is used as baseclass
for other DataManipulator classes.
"""

from typing import Type, TypeVar, Generic
from .context_data import ContextData

from sqlalchemy.future import Engine

T = TypeVar('T')


class DataManipulator(Generic[T]):
    """Class to manipulate database data.

    The DataManipulator class is the baseclass for other DataManipulators.
    Subclasses inherit this class to get a consistent initiator.

    Attributes:
        _database_model: the SQLmodel model used by this DataManipulator.
        _database_engine: the SQLalchemy engine to use.
        _context_data: specifies in what context to use the manipulator.
    """

    def __init__(self,
                 database_model: Type[T],
                 database_engine: Engine,
                 context_data: ContextData) -> None:
        """Set attributes for the class.

        The initiator sets the attributes for the class to the values specified
        in the arguments.

        Args:
            database_model: the SQLmodel model used by this DataManipulator.
            database_engine: the SQLalchemy engine to use.
            context_data: specifies in what context to use the manipulator.
        """
        self._database_model = database_model
        self._database_engine = database_engine
        self._context_data = context_data
