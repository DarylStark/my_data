from sqlmodel import Field, SQLModel, Relationship

from database.database import Database

from my_model.tag import Tag
from my_model.user import User, UserRole


class DBUser(SQLModel, User, table=True):
    # Primary key
    id: int | None = Field(default=None, primary_key=True)

    # Relationships
    tags: list['DBTag'] = Relationship(back_populates='user')


class DBTag(SQLModel, Tag, table=True):
    # Primary key
    id: int | None = Field(default=None, primary_key=True)

    # Relationships
    user_id: int = Field(foreign_key='dbuser.id')
    user: DBUser = Relationship(back_populates='tags')
