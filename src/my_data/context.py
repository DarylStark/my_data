from calendar import c

from my_model.tag import Tag
from my_model.user import User

from .context_data import ContextData
from .resource_manager import ResourceManager, UserGetter
from .db_models import DBUser, DBTag
from types import TracebackType


# TODO: Make this a context manager

class Context:
    def __init__(self,
                 user: User | None = None):

        # Object with the context data in it
        self.context_data = ContextData(user=user)

        # Objects to manage data objects
        self.tags = ResourceManager(model=Tag,
                                    db_model=DBTag,
                                    context_data=self.context_data)

        self.users = ResourceManager(model=User,
                                     db_model=DBUser,
                                     context_data=self.context_data,
                                     getter=UserGetter)

    def __enter__(self) -> 'Context':
        return self

    def __exit__(self,
                 exception_type: BaseException | None,
                 exception_value: BaseException | None,
                 traceback: TracebackType | None) -> bool:
        return exception_type is None
