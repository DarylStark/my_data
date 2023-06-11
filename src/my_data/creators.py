"""The creators for the ResourceManager.

This module contains the Creators for the ResourceManager. It contains the
base-class and the subclasses.
"""
from typing import Type

from .context_data import ContextData


class Creator:
    """Base Creator class.

    The base Creator class should be used as the base class for specific
    Creator-classes. The base class defines the interface for all
    Creator-classes.

    Attributes:
        _contxt_data: the passwed ContextData object.
        _db_model: the database model that should be used to retrieve data.
    """

    def __init__(self, context_data: ContextData, db_model: Type) -> None:
        """Set the specifics for the Creator.

        To create the Creator, a ContextData object is required, and the DB
        model that is used to select data.

        Args:
            context_data: the `ContextData` object for this Creator.
            db_model: the DB Model for the object.
        """
        # TODO: this is the same for Getters as for Creators. They are most
        # probably the same for Updaters and Deleters too. Maybe put these
        # in a generic Base-class?
        self._context_data = context_data
        self._db_model = db_model


class UserSpecificCreator(Creator):
    """Creator for user specific resources.

    This creator should be used for resources that are bound to specific users,
    like tags and API tokens.
    """


class UserCreator(Creator):
    """Creator for user specific resources.

    This creator should be used for resources that are bound to specific users,
    like tags and API tokens.
    """
