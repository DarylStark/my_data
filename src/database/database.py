from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.future import Engine
from .exceptions import DatabaseConnectionError
from sqlalchemy.exc import OperationalError


class Database:

    def __init__(self):
        # Variables from the user. Should be set with `configure`
        self.connection_string: str = 'sqlite:///:memory'
        self.echo: bool = False
        self.pool_pre_ping: bool = True
        self.pool_recycle: int = 10
        self.pool_size: int = 5
        self.pool_overflow: int | None = None

        # Internal objects
        self._engine: Engine | None = None

    def configure(self,
                  connection: str,
                  echo: bool = False,
                  pool_pre_ping: bool = True,
                  pool_recycle: int = 10,
                  pool_size: int = 5,
                  pool_overflow: int | None = None) -> None:

        # Variables from the user
        self.connection_string = connection
        self.echo = echo
        self.pool_pre_ping = pool_pre_ping
        self.pool_recycle = pool_recycle
        self.pool_size = pool_size
        self.pool_overflow = pool_overflow

    def create_engine(self) -> None:
        try:
            # Create the engine arguments
            engine_argumens = {
                'url': self.connection_string,
                'echo': self.echo,
                'pool_pre_ping': self.pool_pre_ping,
                'pool_recycle': self.pool_recycle,
                'pool_size': self.pool_size
            }

            if self.pool_overflow:
                engine_argumens['max_overflow'] = self.pool_overflow

            # Create the engine
            self._engine = create_engine(**engine_argumens)
        except OperationalError as sa_error:
            raise DatabaseConnectionError(
                'Couldn\'t connect to database') from sa_error

    def create_tables(self, drop_tables: bool = False) -> None:
        if drop_tables:
            SQLModel.metadata.drop_all(self._engine)
        SQLModel.metadata.create_all(self._engine)

    def get_session(self, *args, **kwargs) -> Session:
        return Session(self._engine, *args, **kwargs)
