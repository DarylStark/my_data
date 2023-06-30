"""My Data Package.

This package contains the code to create, retrieve, update and delete data from
a database containing the objects for the `my_model` package. To use this
package, the application has to connect to a database first. To do this, the
application should use the `configure` function in the `configure` module:

    from my_data.configure import configure, MyDataConfig

    db_connection = configure(MyDataConfig(
        db_type=DatabaseType.SQLITE_MEMORY
    ))

TODO: Rewrite this documentation

After that, you can optionally create the tables. The tables are defined in the
`db_models` module of this package. To create the tables, use the
`create_tables` method:

    db_connection.create_tables(drop_tables=False)

Then, you can use the database object by using a `Context` object. This object
specifies in what context you want to retrieve data. You can, for example,
specify a user in this context to get only resources that are relevant for this
user. The `Context` object can be used as a context manager:

    from my_model.user_scoped_models import User
    from datetime import datetime

    normal_user = User(
        fullname='Daryl Stark',
        username='daryl.stark',
        email='user@example.com',
        role=UserRole.USER,
        password_hash='xxx',
        password_date=datetime.now())

    with Context(user=normal_user) as user_context:
        tags = user_context.tags.get()
"""

__version__ = '0.0.1-dev'
