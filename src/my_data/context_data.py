from pydantic.dataclasses import dataclass
from my_model.user import User


@dataclass
class ContextData:
    user: User | None = None
