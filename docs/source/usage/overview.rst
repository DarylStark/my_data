Overview
========

The package contains a ``MyData`` class that is the central point of the package. Objects of this class can be used to create, retrieve, update or delete data. To do this, it uses a SQL backend, like MySQL, PostgreSQL, SQLite, etc. You have to configure the object to connect to a specific database. The drivers for specific databases, like PostgreSQL, are not included in this package, but are available as separate packages. For instance, the ``pg8000`` package is a driver for PostgreSQL and should be installed separately.

To give the user of the object access to the components, it has to authorize as either a *normal user*, or a *service user*.

A *normal user* can be a root user or a *normal user*. The only difference in permissions between them, is that a root user can create users. A *service user* cannot create users or other user scoped elements, but can retrieve users by username or API token. This is useful for, for instance, a web application that needs to retrieve data from the database on the behalf of a user.