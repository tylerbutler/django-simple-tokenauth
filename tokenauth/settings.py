# coding=utf-8
from django.conf import settings

# App-specific config options and defaults
SIMPLE_TOKENAUTH_TOKEN_EXPIRY_TIME = getattr(settings, 'SIMPLE_TOKENAUTH_TOKEN_EXPIRY_TIME', 60 * 60 * 2) # 2 hours (60 secs * 60 mins * 2)
"""The time, in seconds, that an :class:`~.models.AccessToken` should stay valid after creation."""
