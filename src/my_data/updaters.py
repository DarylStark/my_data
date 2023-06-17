"""The updaters for the ResourceMAaager.

This module contains the Updaters for the ResourceManager. It contains the
base-class and the subclasses.
"""

from my_model._model import Model  # type: ignore
from my_model.user import UserRole  # type: ignore
from sqlmodel import SQLModel

from my_data.db_connection import db_connection

from .crud_base import CRUDBase
from .exceptions import InvalidModelException, PermissionDeniedException


class Updater(CRUDBase):
    """Base Updater class.

    The base Updater class should be used as the base class for specific
    Updater-classes. The base class defines the interface for all
    Updater-classes.
    """

    def get_db_model(self, data: Model) -> SQLModel:
        """Get the `db_model` from the given model.

        Returns the (hidden) DB model in the given model. This DB model gets
        hidden in there when retrieving the data. We need the DB model to
        update the database. This method also updates the DB model with the
        values from the given model.

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
            # Update the fields
            for fieldname, _ in data.__fields__.items():
                setattr(model, fieldname, getattr(data, fieldname))

            # Return the new model
            return model

        # No connected DB model
        raise InvalidModelException(
            'The model is not retrieved via the `my-data` package.')

    def update(self, models: list[Model] | Model) -> list[Model]:
        """Update the model in the database.

        Updates the model in the database. This method executes the queries in
        the database to update the row.

        Args:
            models: the models to update.

        Returns:
            Model: the updated models.
        """
        if not isinstance(models, list):
            models = [models]

        # Convert them to the DB models
        db_models = [self.get_db_model(model) for model in models]

        # Update them in the database
        with db_connection.get_session() as session:
            for model in db_models:
                session.add(model)
            session.commit()

        # Return the new models
        return models


class UserSpecificUpdater(Updater):
    """Updater for user specific resources.

    This updater should be used for resources that are bound to specific users,
    like tags and API tokens.
    """

    def get_db_model(self, data: Model) -> SQLModel:
        """Get the `db_model` from the given model.

        Retrieves the DB model from the given model using the `get_db_model`
        method in the base class. It then uses the `user_id` field in the model
        to check if this user is allowed to change this resource. If the user
        is not allowed to change this resouce, a exception is raieed.

        Args:
            data: the `my-model` instance.

        Returns:
            The DB model with the updated fields.

        Raises:
            PermissionDeniedException: when the user in the context has no
                permissions to update this resource.
        """
        model = super().get_db_model(data)
        if model.user_id == self._context_data.user.id:
            return model
        raise PermissionDeniedException(
            f'User "{self._context_data.user.username}" is not allowed to ' +
            'update reousrce ID "{model.id}"')


class UserUpdater(Updater):
    """Updater for user resources.

    This updater should be used to update users.
    """

    def get_db_model(self, data: Model) -> SQLModel:
        """Get the `db_model` from the given model.

        Checks if this user is allowed to change the user resource. A ROOT user
        can change all user resources. Other users can only change their own
        user resource.

        Args:
            data: the `my-model` instance.

        Returns:
            The DB model with the updated fields.

        Raises:
            PermissionDeniedException: when the user in the context has no
                permissions to update this resource.
        """
        model = super().get_db_model(data)
        if self._context_data.user.role == UserRole.ROOT or (
            model.id == self._context_data.user.id
        ):
            return model
        raise PermissionDeniedException(
            f'User "{self._context_data.user.username}" is not allowed to ' +
            'update user ID "{model.id}"')
