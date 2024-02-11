REST API Service example
========================

This page describes a small example on how to use this library to create a REST API service. It doesn't document a complete REST API service, but it gives the basic steps to create a REST API service using ``MyData``. It assumes some library to create the REST API service, like ``Flask``. We use a SQLite database in this example and assume that the schema is already created in the database. We also assume that the database is filled with data. In the database will be a service user (username ``rest_api_service`` with password ``rest_api_password``) and a user with the username ``daryl.stark``. This user is a *normal user*.

Create the database connection
------------------------------

First, we have to create the database connection. To do this, we import the ``MyData`` class, initiate and configure it.

.. code-block:: python

    from typing import Optional
    from my_model import Tag, APIToken
    from my_data import MyData
    from my_data.authorization import APITokenAuthorizer
    from my_data.authenticator import UserAuthenticator, CredentialsAuthenticator

    mydata = MyData()
    mydata.config(
        db_url='sqlite:///mydata.db',
        service_username='rest_api_service',
        service_password='rest_api_password'
    )

Add a authentication endpoint
-----------------------------

Then, we can add a endpoint to authenticate a user. First, we check if the user is not logged on yet. We use the ``UserAuthenticator`` to authenticate the user and create a API token. The API token is returned to the user. If the authentication fails, a ``AuthenticationError`` is raised.

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
            my_data_object=mydata,
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

Add a endpoint to logoff the current user
-----------------------------------------

Then, we add an endpoint to logoff the current user. We use the ``APITokenAuthorizer`` to authorize the user with a ``ShortLivedTokenAuthorizer``. This authorizer will only authorize succesfully if the user is using a short lived token. If the user is authorized, we logoff the user and return a dictionary to indicate that the user is logged off.

.. code-block:: python

    @api_library.endpoint('/logoff', methods=['POST'])
    def logoff(api_token: Optional[str] = None):
        """Endpoint to logoff the current user.
        
        Args:
            api_token: a API token, if the user gave one.
        """
        # Authorize the user. The given token needs to be a short lived token.
        authorizer = APITokenAuthorizer(
            my_data_object=mydata,
            api_token=api_token,
            authorizer=ShortLivedTokenAuthorizer())
        authorizer.authorize()

        # Logoff the user
        with mydata.get_context(user=authorizer.user) as context:
            context.api_tokens.delete(APIToken.token=api_token)

        # Return a dictionary to indicate that the user is logged off.
        return {'logged_off': True}

Endpoints to manage data
------------------------

Now we can add endpoints to manage the data. We use the ``APITokenAuthorizer`` to authorize the user. If the user is not authorized, a ``AuthorizationError`` is raised. If the user is authorized, the endpoint is executed and we can retrieve the data from the database. We also specify that short lived tokens are allowed.

Creating tags
~~~~~~~~~~~~~

First, we add an endpoint to create a tag. We use the ``APITokenAuthorizer`` to authorize the user. The given token needs to have the ``tags.create`` scope. If the user is authorized, we create the tag and return it.

.. code-block:: python

    @api_library.endpoint('/tags', methods=['POST'])
    def create_tag(
        title: str, api_token: Optional[str] = None):
        """Endpoint to create a tag.
        
        Args:
            title: the title of the tag to create.
            api_token: a API token, if the user gave one.
        """
        # Authorize the user. The given token needs to have the 'tags.create' scope.
        authorizer = APITokenAuthorizer(
            my_data_object=mydata,
            api_token=api_token,
            authorizer=APIScopeAuthorizer(
                required_scopes=['tags.create'],
                allow_short_lived=True
            ))
        authorizer.authorize()
        
        # Create the tag
        with mydata.get_context(user=authorizer.user) as context:
            tag = context.tags.create(title=title)
        
        # Return the created tag
        return tag

Retrieving tags
~~~~~~~~~~~~~~~

Then, we add an endpoint to retrieve all tags for the user. We use the ``APITokenAuthorizer`` to authorize the user. The given token needs to have the ``tags.retrieve`` scope. If the user is authorized, we retrieve the data from the database and return it.

.. code-block:: python

    @api_library.endpoint('/tags', methods=['GET'])
    def retrieve_tags(
        title: Optional[str] = None, api_token: Optional[str] = None):
        """Endpoint to retrieve all tags for the user.
        
        Args:
            title: filter on title.
            api_token: a API token, if the user gave one.
        """
        # Authorize the user. The given token needs to have the 'tags.retrieve' scope.
        authorizer = APITokenAuthorizer(
            my_data_object=mydata,
            api_token=api_token,
            authorizer=APIScopeAuthorizer(
                required_scopes=['tags.retrieve'],
                allow_short_lived=True
            ))
        authorizer.authorize()
        
        # Retrieve the data from the database
        with mydata.get_context(user=authorizer.user) as context:
            flt = None
            if title:
                flt = Tag.title == title
            tags = context.tags.retrieve(flt=flt)
        
        # Return the retrieved data
        return tags

Updating tags
~~~~~~~~~~~~~

Then, we add an endpoint to update a tag. We use the ``APITokenAuthorizer`` to authorize the user. The given token needs to have the ``tags.update`` scope. If the user is authorized, we update the tag and return it.

.. code-block:: python
    
    @api_library.endpoint('/tags', methods=['PUT'])
    def update_tag(
        title: str, new_title: str, api_token: Optional[str] = None):
        """Endpoint to update a tag.
        
        Args:
            title: the title of the tag to update.
            new_title: the new title for the tag.
            api_token: a API token, if the user gave one.
        """
        # Authorize the user. The given token needs to have the 'tags.update' scope.
        authorizer = APITokenAuthorizer(
            my_data_object=mydata,
            api_token=api_token,
            authorizer=APIScopeAuthorizer(
                required_scopes=['tags.update'],
                allow_short_lived=True
            ))
        authorizer.authorize()
        
        # Retrieve the data and update it
        with mydata.get_context(user=authorizer.user) as context:
            tags = context.tags.retrieve(flt=Tag.title == title)
            for tag in tags:
                tag.title = new_title
            tags = context.tags.update(tags)
        
        # Return the updated tag
        return tags

Deleting tags
~~~~~~~~~~~~~

Finally, we add an endpoint to delete a tag. We use the ``APITokenAuthorizer`` to authorize the user. The given token needs to have the ``tags.delete`` scope. If the user is authorized, we delete the tag and return a dictionary to indicate that the tag is deleted.

.. code-block:: python
    
    @api_library.endpoint('/tags', methods=['DELETE'])
    def delete_tag(
        title: str, api_token: Optional[str] = None):
        """Endpoint to delete a tag.
        
        Args:
            title: the title of the tag to delete.
            api_token: a API token, if the user gave one.
        """
        # Authorize the user. The given token needs to have the 'tags.delete' scope.
        authorizer = APITokenAuthorizer(
            my_data_object=mydata,
            api_token=api_token,
            authorizer=APIScopeAuthorizer(
                required_scopes=['tags.delete'],
                allow_short_lived=True
            ))
        authorizer.authorize()
        
        # Retrieve the data and delete it
        with mydata.get_context(user=authorizer.user) as context:
            tags = context.tags.retrieve(flt=Tag.title == title)
            context.tags.delete(tags)
        
        # Return a dictionary to indicate that the tag is deleted.
        return {'deleted': True}

