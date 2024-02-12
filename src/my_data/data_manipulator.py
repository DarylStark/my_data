"""Module with the DataManipulator class.

This module contains the DataManipulator class. This class is used as baseclass
for other DataManipulator classes.
"""
import logging
from typing import Generic, Type, TypeVar

from sqlalchemy.future import Engine

from my_model import UserScopedModel

from .context_data import ContextData
from .exceptions import (PermissionDeniedException,
                         WrongDataManipulatorException)

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
        self._logger = logging.getLogger(f'DataManipulator-{id(self)}')
        self._database_model = database_model
        self._database_engine = database_engine
        self._context_data = context_data

    def _convert_model_to_list(self, models: list[T] | T) -> list[T]:
        """Convert a model to a list of models.

        Method to convert a model to a list of models, unless it already is a
        list.

        Args:
            models: the model(s).

        Returns:
            A list with models.
        """
        if not isinstance(models, list):
            return [models]
        return models

    def _validate_user_scoped_models(self, models: list[T] | T) -> list[T]:
        """Validate model type and user ID in user scoped models.

        Method to validate if a User Scoped model is a subclass of the
        baseclass UserScopedModel and if the `user_id` field in the data is set
        to the user in the context.

        Args:
            models: the models to check.

        Raises:
            WrongDataManipulatorException: when the model in the instance is
                not a UserScopedModel.
            PermissionDeniedException: when the model is not the same model as
                set in the instance or when the model has a user_id set that is
                different then the current user_id in the context.

        Returns:
            A list with the resources.
        """
        # Check if it is a subtype of UserScopedModel
        if not issubclass(self._database_model, UserScopedModel):
            raise WrongDataManipulatorException(  # pragma: no cover
                f'The model "{self._database_model}" is not a UserScopedModel')

        # Make sure the `models` are always a list
        models = self._convert_model_to_list(models)

        # Verify the model type and if the `user_id` field is set.
        for model in models:
            if not isinstance(model, self._database_model):
                raise PermissionDeniedException(  # pragma: no cover
                    f'Expected "{self._database_model}", got "{type(model)}".')

            if getattr(model, 'user_id', None) != self._context_data.user.id:
                raise PermissionDeniedException(  # pragma: no cover
                    'This user is not allowed to alter this resource')

        return models

    def _add_models_to_session(self, models: list[T] | T) -> list[T]:
        """Add models to a session and commit the session.

        Method to add models a SQLalchemy session and commit the session. This
        can be used for adding or updating resources.

        Args:
            models: the models to add.

        Returns:
            The list of models.
        """
        # Make sure the `models` are always a list
        if not isinstance(models, list):
            models = [models]

        # Update the resources
        for model in models:
            self._context_data.db_session.add(model)
        return models
