Authentication
==============

The library contains a class to authenticate users. This class can be used by the application to authenticate users. The class is called ``UserAuthenticator`` and uses a *strategy* pattern to authenticate users. This means that the way authentication is done, can be changed during runtime. If you want to create a own authenticator to use with this class, you can do so by creating a class that inherits from the ``Authenticator`` class.

When creating a instance of the ``UserAuthenticator`` class, you have to pass a instance of the ``MyData`` class and instance of a class that inherits from the ``Authenticator`` class. This instance will be used to authenticate users. Right now, one authenticator is created. This authenticator, named ``CredentialsAuthenticator`` should be used to authenticate users based on their credentials in the database. These credentials are a *username*, *password* and optionally and *second factor*.

**For example:**

.. code-block:: python

    from authenticator import UserAuthenticator, CredentialsAuthenticator

    authenticator = CredentialsAuthenticator(
        username='user',
        password='password',
        second_factor='123456')
    user_authenticator = UserAuthenticator(
        my_data,
        authenticator)
    user = user_authenticator.authenticate()

If the authentication is a success, the ``user`` object will now be the object for the user that is given. If the authentication is not a success, a ``AuthenticationError`` will be raised.

.. warning::

    If the given user has a ``second_factor`` defined but the the second factor is not given in the initializer of the ``CredentialsAuthenticator``, the authentication will fail, even if the password is correct!

You can also use the ``UserAuthenticator`` class to create short lived API Tokens for authenticated users. This is usefull if you want to create a API token for the user that just authenticated. To do this, use the ``create_api_token`` method of the ``UserAuthenticator`` class. This method will return a string that can be used as a API token for the user. You have to specify how long the token will be valid (in seconds) and a title for the token:

.. code-block:: python

    from authenticator import UserAuthenticator, CredentialsAuthenticator

    authenticator = CredentialsAuthenticator(
        username='user',
        password='password',
        second_factor='123456')
    user_authenticator = UserAuthenticator(
        my_data,
        authenticator)
    token_str = user_authenticator.create_api_token(
        session_timeout_in_seconds=3600,   # token will be valid for 1 hour
        title='my interactive token')

The method will authenticate the user for you, so you don't have to call the ``authenticate`` method before calling the ``create_api_token`` method.

Creating own authenticators
---------------------------

It is possible to create own authenticator that authenticate users based on different information. This way, it is possible to create authenticators that use webauth for instance. To do this, create a class that inherits from the ``Authenticator`` class and override the ``authenticate`` method. This method should return the user object if the authentication is a success, or raise a ``AuthenticationError`` if the authentication is not a success. You can then pass a instance of the created object to the ``UserAuthenticator`` class.