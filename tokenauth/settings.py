# coding=utf-8
from django.conf import settings

# App-specific config options and defaults
SIMPLE_TOKENAUTH_TOKEN_EXPIRY_TIME = getattr(settings, 'SIMPLE_TOKENAUTH_TOKEN_EXPIRY_TIME', 60 * 60 * 2) # 2 hours (60 secs * 60 mins * 2)
"""The time, in seconds, that an :class:`~.models.AccessToken` should stay valid after creation."""

SIMPLE_TOKENAUTH_AUTO_DELETE = getattr(settings, 'SIMPLE_TOKENAUTH_AUTO_DELETE', True)
"""If ``True``, an expired access token will be proactively deleted from the database when the
:attr:`~.models.AccessToken.expired` property is accessed or the :meth:`~.models.AccessToken.validate`
method is called.

If this is set to ``False``, access tokens will *only* be deleted if :meth:`~.models.AccessToken.create_token` is
called and there is an expired access token already present for the user/resource combination. In this case,
the old token will be deleted, but a new one will be created in its place immediately.
"""
