.. _tokenauth:

:currentmodule: tokenauth

django-simple-tokenauth
=======================

The ``tokenauth`` app provides a set of models, decorators, and a custom authentication backend that can be used to
add simple token-based authentication to a Django project.

An :class:`~.models.AccessToken` has the following characteristics:

1. It is valid for a *single* :class:`~django.contrib.auth.models.User` and resource combination.
2. It expires after a period of time automatically. By default this is two hours but it's configurable.

.. ..contents::
   :depth: 2
   :local:

Installation
------------
To install, use pip directly against the git repository::

    pip install git+git://github.com/tylerbutler/django-simple-tokenauth.git

Configuration
-------------
1. Add the ``tokenauth`` package to the ``INSTALLED_APPS`` setting of your Django project.
2. Add the :class:`tokenauth.backends.AccessTokenAuthenticationBackend` to the ``AUTHENTICATION_BACKENDS`` setting
   of your project.
3. Optionally set the :data:`~.settings.SIMPLE_TOKENAUTH_TOKEN_EXPIRY_TIME` value if you want to override the default
   of two hours.

For example, you might have something like the following in your Django settings file::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.sites',
        'tokenauth',
        # ...other installed applications...
    )

    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'tokenauth.backends.AccessTokenAuthenticationBackend',
        )

    SIMPLE_TOKENAUTH_TOKEN_EXPIRY_TIME = 3600 #1 hour expiry time.

Once you've done this, run ``manage.py syncdb`` to install the ``tokenauth`` models.

Settings
--------

.. automodule:: tokenauth.settings
   :members:

Usage
-----

.. .. :currentmodule: tokenauth.models

Creating an AccessToken
~~~~~~~~~~~~~~~~~~~~~~~
In order to create an access token, use the :meth:`~.AccessToken.create_token` method::

    from tokenauth.models import AccessToken

    token = AccessToken.create_token(resource, user)


Validating an AccessToken
~~~~~~~~~~~~~~~~~~~~~~~~~
Validating an access token can be done using the :meth:`~.AccessToken.validate` method::

    from tokenauth.models import AccessToken

    is_valid, token = AccessToken.validate(access_token_as_string, resource_id)
    if is_valid:
        ... # do something
    else:
        ... # do something else


Getting an AccessToken Object from a String
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In many cases an access token will come in the form of a string. In order to translate it into an
:class:`~.AccessToken` object, use the :meth:`~.AccessToken.validate` method as described in the
previous example. The method returns a 2-tuple, the second value of which is the access token itself,
assuming the token was valid.

API Reference
-------------

Models
~~~~~~

.. autoclass:: tokenauth.managers.AccessTokenManager
   :members:

.. autoclass:: tokenauth.models.AccessToken
   :members:
  
Decorators
~~~~~~~~~~

.. automodule:: tokenauth.decorators
   :members:

Backends
~~~~~~~~

.. automodule:: tokenauth.backends
   :members:
