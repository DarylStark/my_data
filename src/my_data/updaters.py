"""The updaters for the ResourceMAaager.

This module contains the Updaters for the ResourceManager. It contains the
base-class and the subclasses.
"""

from dataclasses import field
from my_model._model import Model  # type: ignore
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

    def update(self, models: list[Model] | Model) -> None:
        """Update the model in the database.

        Updates the model in the database. This method executes the queries in
        the database to update the row.

        Args:
            models: the models to update.
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


class UserSpecificUpdater(Updater):
    """Updater for user specific resources.

    This updater should be used for resources that are bound to specific users,
    like tags and API tokens.
    """

    def get_db_model(self, data: Model) -> SQLModel:
        model = super().get_db_model(data)
        if model.user_id == self._context_data.user.id:
            return model
        raise PermissionDeniedException(
            f'User "{self._context_data.user.username}" is not allowed to update tag ID "{model.id}"')


class UserUpdater(Updater):
    """Updatar for user resources.

    This updater should be used to updater users.
    """
    # TODO: Make sure the user is allowed to update this item
