Authentication
==============

The library contains a class to authenticate users. This class can be used by the application to authenticate users. The class is called ``UserAuthenticator`` and uses a Strategy pattern to authenticate users. The class has a method ``authenticate`` that takes a username and password and returns a ``User`` object if the user is authenticated. If the user is not authenticated, the method returns ``None``. By setting a specific Authenticator, the way authentication is done is specified. The library contains one Authenticator: the ``CredentialsAutheticator``. This ``Authenticator`` can be used to authenticate users based on username, password and optionally the second factor.

Example
-------

.. code-block:: python

    from my_data.authenticator import UserAuthenticator, CredentialsAuthenticator

    # Authenticate a user
    user_authenticator = UserAuthenticator(CredentialsAuthenticator(
        username='test_username',
        password='password'
        # Optionally, you can specify a second factor here
    ))
    user_authenticator.authenticate()
    # Will raise AuthenticationFailed when the user is not authenticated.