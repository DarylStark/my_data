"""TODO: documentation."""
from types import TracebackType

from sqlalchemy.future import Engine

from .context_data import ContextData


class Context:
    """TODO: documentation."""

    def __init__(self,
                 database_engine: Engine,
                 context_data: ContextData) -> None:
        """TODO: documentation."""
        self.database_engine = database_engine
        self._context_data = context_data

    def __enter__(self) -> 'Context':
        """TODO: documentation."""
        return self

    def __exit__(self,
                 exception_type: BaseException | None,
                 exception_value: BaseException | None,
                 traceback: TracebackType | None) -> bool:
        """TODO: documentation."""
        return exception_type is None
