"""My Data Package.

This package contains the code to create, retrieve, update and delete data from
a database containing the objects for the `my_model` package.

To use this package, you have to use the MyData class, which is located in the
`my_data` module. After creating a instance of this class, you have to
configure it with the correct database string and additional arguments. These
arguments are all used by SQLmodel (and SQLalchemy) to create the correct
engine to connect to the database.

An example:

```python
from my_data import

# Configure the database
my_data = MyData()
my_data.configure(
    # db_connection_str='sqlite:///:memory:',
    db_connection_str='sqlite:////home/dast/my.sqlite',
    database_args={
        'echo': True,
        'pool_pre_ping': True,
        'pool_recycle': True,
    }
)

# Create the engine and the test data
my_data.create_engine()
```

You can now use the package. If you need to create the tables, you can use the
`create_db_tables` method:

```python
my_data.create_db_tables()
```

If you want to create initial data, for testing or when initializing the
database, you can use the `create_init_data` tables. _Warning:_ this will
remove all tables in the database first, so use with care!

```python
my_data.create_init_data()
```

After that, a Context can be used to manipulate data in the database:

```python
with my_data.get_context(user=root_user) as c:
    all_users = c.user.retrieve()
```
"""

from .my_data import MyData  # noqa: F401

__version__ = '1.0.0'
