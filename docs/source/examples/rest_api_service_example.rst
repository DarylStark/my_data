REST API Service example
========================

This page describes a small example on how to use this library to create a REST API service. It doesn't document a complete REST API service, but it gives the basic steps to create a REST API service using ``MyData``. It assumes some library to create the REST API service, like ``Flask``. We use a SQLite database in this example and assume that the schema is already created in the database. We also assume that the database is filled with data. In the database will be a service user (username ``rest_api_service`` with password ``rest_api_password``) and a user with the username ``daryl.stark``. This user is a *normal user*.

Create the database connection
------------------------------

First, we have to create the database connection. To do this, we import the ``MyData`` class, initiate and configure it. We also configure the ``UserAuthenticator`` and ``APITokenAuhtorizer`` classes.

.. code-block:: python

    from typing import Optional
    from my_model import User
    from my_data import MyData
    from my_data.authorization import APITokenAuthorizer
    from my_data.authenticator import UserAuthenticator, CredentialsAuthenticator

    mydata = MyData()
    mydata.config(
        db_url='sqlite:///mydata.db'
    )

    # Configure UserAuthenticator
    UserAuthenticator.configure(
        mydata=mydata,
        service_username='rest_api_service',
        service_password='rest_api_password')
    
    # Configure APITokenAuthorizer
    APITokenAuthorizer.configure(
        mydata=mydata,
        service_username='rest_api_service',
        service_password='rest_api_password')

Add a authentication endpoint
-----------------------------

Then, we can add a endpoint to authenticate a user. Firstwe check if the user is not logged on yet. We use the ``UserAuthenticator`` to authenticate the user and create a API token. The API token is returned to the user. If the authentication fails, a ``AuthenticationError`` is raised.

.. code-block:: python

    api_library = APILibrary(title='My REST API')

    @api_library.endpoint('/login', methods=['POST'])
    def login(username: str, password: str, api_token: Optional[str] = None):
        """Endpoint to authenticate a user.
        
        Args:
            username: the username for the user.
            password: the password for the user.
            api_token: a API token, if the user gave one.
        """
        # Make sure the user is not logged on yet
        authorizer = APITokenAuthorizer(
            api_token=api_token,
            authorizer=InvalidTokenAuthorizer())
        authorizer.authorize()

        # Auhenticate the user
        authenticator = CredentialsAuthenticator(
            username=username,
            password=password)
        user_authenticator = UserAuthenticator(authenticator)

        # Create a short lived API token for the user
        token_str = user_authenticator.create_api_token(
            session_timeout_in_seconds=3600,   # token will be valid for 1 hour
            title='my interactive token')

        # Return the given token
        return {'token': token_str}

Endpoints to manage data
------------------------

Now we can add endpoints to manage the data. We use the ``APITokenAuthorizer`` to authorize the user. If the user is not authorized, a ``AuthorizationError`` is raised. If the user is authorized, the endpoint is executed and we can retrieve the data from the database.

.. code-block:: python

    @api_library.endpoint('/users', methods=['GET'])
    def get_users(
        username: Optional[str] = None, api_token: Optional[str] = None):
        """Endpoint to retrieve all users the user is allowed to see.
        
        Args:
            username: filter on username.
            api_token: a API token, if the user gave one.
        """
        # Authorize the user
        authorizer = APITokenAuthorizer(
            api_token=api_token,
            authorizer=APIScopeAuthorizer(
                required_scopes=['users.retrieve'],
                allow_short_lived=True
            ))
        authorizer.authorize()
        
        # Retrieve the data
        with mydata.get_context(user=authorizer.user) as context:
            flt = None
            if username:
                flt = User.username == username
            users = context.users.retrieve(flt=flt)
        
        # Return the retrieved data
        return users
    
    @api_library.endpoint('/users', methods=['DELETE'])
    def delete_user(
        username: str, api_token: Optional[str] = None):
        """Endpoint to delete a user.
        
        Args:
            username: the username to delete
            api_token: a API token, if the user gave one.
        """
        # Authorize the user
        authorizer = APITokenAuthorizer(
            api_token=api_token,
            authorizer=APIScopeAuthorizer(
                required_scopes=['users.delete'],
                allow_short_lived=True
            ))
        authorizer.authorize()
        
        # Retrieve the data and delete it
        with mydata.get_context(user=authorizer.user) as context:
            users = context.users.retrieve(flt=User.username == username)
            context.users.delete(users)
        
        # Return the retrieved data
        return users

It is easy to add new endpoints to create or update users from this point on.