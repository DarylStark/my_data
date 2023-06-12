"""Module with the CRUDBase class.

The class in this module can and should be used as base class for CRUD classes,
like getters and creators.
"""

from typing import Type
from .context_data import ContextData


class CRUDBase:
    """Base class for CRUD classes.

    Contains the base attributes for the CRUD classes like getters, creators,
    updaters and deleters. The base classes for these type of objects should
    inherit this class to get a consistent interface.

    Attributes:
        _context_data: the passed ContextData object.
        _model: the `my-model` model that should be used for this manager.
        _db_model: the database model that should be used to retrieve data.
    """

    def __init__(self,
                 context_data: ContextData,
                 model: Type, db_model: Type) -> None:
        """Set the specifics for the Getter.

        To create the Getter, a ContextData object is required, and the DB
        model that is used to select data.

        Args:
            context_data: the `ContextData` object for this Getter.
            model: the `my-model` model for the project.
            db_model: the DB Model for the object.
        """
        self._context_data = context_data
        self._model = model
        self._db_model = db_model
