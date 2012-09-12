# coding=utf-8
import uuid
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from tokenauth import settings
from tokenauth.managers import AccessTokenManager

class AccessToken(models.Model):
    """
    An access token representing a :class:`~django.contrib.auth.models.User` and a resource.
    Resources can be any Django model thanks to the Content Types framework provided by Django.

    .. seealso:: :class:`~tokenauth.managers.AccessTokenManager`
    """
    class Meta:
        unique_together = (('token', 'user'),)
    objects = AccessTokenManager()

    _content_type = models.ForeignKey(ContentType)
    _object_id = models.PositiveIntegerField()
    resource = generic.GenericForeignKey('_content_type', '_object_id')
    user = models.ForeignKey(User)
    _time_issued = models.DateTimeField(default=timezone.now)
    token = models.CharField(max_length=512, unique=True, default=uuid.uuid4)

    @property
    def time_issued(self):
        """The time the access token was issued or refreshed."""
        return self._time_issued

    @time_issued.setter
    def time_issued(self, value):
        if timezone.is_naive(value):
            value = timezone.make_aware(value, timezone.utc)
        self._time_issued = value

    @property
    def expired(self):
        """Returns ``True`` if the access token has expired, ``False`` otherwise. *Read-only property.*"""
        if timezone.now() > self.expiry_time:
            return True
        else:
            return False

    @property
    def expiry_time(self):
        """The expiry time of the access token. *Read-only property.*"""
        return self.time_issued + timedelta(seconds=settings.SIMPLE_TOKENAUTH_TOKEN_EXPIRY_TIME)

    def __unicode__(self):
        return unicode(self.token)

    @classmethod
    def create_token(cls, resource, user):
        """
        Convenience method; shortcut to
        :func:`AccessTokenManager.create_token<tokenauth.managers.AccessTokenManager.create_token>`.
        """
        return cls.objects.create_token(resource, user)

    @classmethod
    def validate(cls, access_token, resource_id):
        """
        Convenience method; shortcut to
        :func:`AccessTokenManager.validate<tokenauth.managers.AccessTokenManager.validate>`.
        """
        return cls.objects.validate(access_token, resource_id)
