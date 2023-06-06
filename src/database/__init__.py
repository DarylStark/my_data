"""Initializer for `database` package.

This package contains a wrapper for SQLModel. This wrapper makes it more
convinient to use SQLModel in a bigger application. The user has to create a
(global) object to connect to his database using the following code:


    from database import Database
    db = Database()
    db.configure('sqlite:///:memory:')
    db.create_engine()

After that, he can create the tables. To do this, the tables have to be defined
first using the SQLModel baseclass:

    class Movie(SQLModel, table=True):
        id: int | None = None
        name: str
        director: str

        db.create_tables(drop_tables=True)

To use this Database, the user has to create a `Session`. To do this, I created
a factory method with the name `get_session()`. The `Session` object can be
used as a Context Manager:

    with db.get_session() as s:
        s.add(Movie(name='Star Wars', director='George Lucas')
        s.commit()
"""

from database.database import Database  # noqa:F401 (Flake: 'unused import')
