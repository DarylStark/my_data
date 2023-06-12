"""Module for DB models.

This module contains the DB models that SQLModel will use for its ORM objects.
These models are based from the models in the `my-model` package and add the
functionality that is needed to be stored in a SQL database. We create seperate
classes for this to seperate the real models from the database models.

Because we use SQLModel, we can easily convert the models between `my-model`
and these database models.
"""
from my_model.tag import Tag  # type: ignore
from my_model.user import User  # type: ignore
from sqlmodel import Field, Relationship, SQLModel


class DBUser(SQLModel, User, table=True):
    """Model for Users.

    Attributes:
        id: the primary key for the User.
        tags: a list of tags for the user, specified in the `DBTag` class.
    """

    # Primary key
    id: int | None = Field(default=None, primary_key=True)

    # Relationships
    tags: list['DBTag'] = Relationship(back_populates='user')


class DBTag(SQLModel, Tag, table=True):
    """Model for Tags.

    Attributes:
        id: the primary key for the Tag.
        user_id: the id for the connected user.
        user: the connected User.
    """

    # Primary key
    id: int | None = Field(default=None, primary_key=True)

    # Relationship fields
    user_id: int | None = Field(foreign_key='dbuser.id')

    # Relationships
    user: DBUser = Relationship(back_populates='tags')
