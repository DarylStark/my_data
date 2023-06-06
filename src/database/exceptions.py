# TODO: Rename everything to 'Exception'


class DatabaseError(Exception):
    """ Base exception for Database-exceptions """
    pass


class DatabaseCriticalError(DatabaseError):
    """ Exception that should result in complete termination of the
        application """
    pass


class DatabaseConnectionError(DatabaseCriticalError):
    """ Error that happends when the database credentials are not
        correct """
    pass
