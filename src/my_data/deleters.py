"""The deleters for the ResourceManager.

This module contains the Deleters for the ResourceManager. It contains the
base-class and the subclasses.
"""

from my_model._model import Model  # type: ignore
from my_model.user import UserRole  # type: ignore
from sqlmodel import SQLModel

from my_data.db_connection import db_connection
from my_data.exceptions import PermissionDeniedException

from .crud_base import CRUDBase
from .exceptions import InvalidModelException


class Deleter(CRUDBase):
    """Base Deleter class.

    The base Deleter class should be used as the base class for specific
    Deleter-classes. The base class defines the interface for all
    Deleter-classes.
    """

    def get_db_model(self, data: Model) -> SQLModel:
        """Get the `db_model` from the given model.

        Returns the (hidden) DB model in the given model. This DB model gets
        hidden in there when retrieving the data. We need the DB model to
        delete from the database.

        Args:
            data: the `my-model` instance.

        Returns:
            The DB model with the updated fields.

        Raises:
            InvalidModelException: when the given model has no hidden DB model.
        """
        # Get the connected DB model
        model: SQLModel = data.get_hidden('db_model')
        if model:
            # Return the new model
            return model

        # No connected DB model
        raise InvalidModelException(
            'The model is not retrieved via the `my-data` package.')

    def delete(self, models: list[Model] | Model) -> None:
        """Delete the model from the database.

        Deletes the model from the database. This method executes the queries
        in the database to delete the row.

        Args:
            models: the models to delete.
        """
        if not isinstance(models, list):
            models = [models]

        # Convert them to the DB models
        db_models = [self.get_db_model(model) for model in models]

        # Update them in the database
        with db_connection.get_session() as session:
            for model in db_models:
                session.delete(model)
            session.commit()


class UserSpecificDeleter(Deleter):
    pass


class UserDeleter(Deleter):
    """Deleter for user resources.

    This deleter should be used to delete users.
    """

    def get_db_model(self, data: Model) -> SQLModel:
        """Get the `db_model` from the given model.

        Checks if this user is allowed to delete the user resource. A ROOT user
        can delete all user resources. Other users can delete no users.

        Args:
            data: the `my-model` instance.

        Returns:
            The DB model for the given model.

        Raises:
            PermissionDeniedException: when the user in the context has no
                permissions to update this resource.
        """
        model = super().get_db_model(data)
        if self._context_data.user.role == UserRole.ROOT:
            return model
        raise PermissionDeniedException(
            f'User "{self._context_data.user.username}" is not allowed to ' +
            'update user ID "{model.id}"')
