from typing import Any

from my_model._model import Model
from sqlmodel import select, SQLModel
from my_data.context_data import ContextData

from .db_connection import _db_connection

from my_model.user import User, UserRole
from .db_models import DBUser


class Getter:
    def __init__(self, context_data, db_model):
        self._context_data = context_data
        self._db_model = db_model

    def filters(self):
        raise NotImplementedError('Filters are not implemented for this type')

    def get(self, *args, **kwargs) -> list[SQLModel]:
        with _db_connection.get_session() as s:
            resources = select(self._db_model)
            for flt in self.filters():
                resources = resources.where(flt)
            results = s.exec(resources)
            return list(results)


class UserSpecificGetter(Getter):
    """Getter for user specific resources."""

    def filters(self):
        if self._context_data is None:
            return list()

        filters: list = list()  # TODO: Better type hinting
        if self._context_data.user:
            filters.append(
                self._db_model.user_id == self._context_data.user.id)
        return filters


class UserGetter(Getter):
    """Getter for user resources."""

    def filters(self):
        if self._context_data is None:
            return list()
        filters: list = list()  # TODO: Better type hinting
        if self._context_data.user:
            if self._context_data.user.role == UserRole.USER:
                filters.append(
                    DBUser.id == self._context_data.user.id
                )
        return filters


class ResourceManager:
    def __init__(self,
                 model: Model,
                 db_model: Any,  # TODO: make this a real type
                 context_data: ContextData | None = None,
                 getter=UserSpecificGetter):

        self._model: Model = model
        self._db_model: Any = db_model
        self._context_data: ContextData | None = context_data

        self.getter: Getter = getter(
            context_data=self._context_data,
            db_model=self._db_model)

    def get(self) -> list[Model]:
        # Get all DB objects from the database
        resources = self.getter.get()

        # Convert the resources to 'my_model' models
        new_resources: list[Model] = [
            self._model(**x.dict())
            for x in resources
        ]

        return new_resources
