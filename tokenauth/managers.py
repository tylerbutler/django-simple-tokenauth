# coding=utf-8
from django.contrib.contenttypes.models import ContentType
from django.db import models

class AccessTokenManager(models.Manager):
    def create_token(self, resource, user):
        """
        Creates an access token for a given user and resource.

        This method should *always* be used to create access tokens instead of creating instances directly and saving
        them. In addition to smoothing over some potentially confusing intricacies of using the Content Types
        framework, it reuses existing tokens when possible.

        :param resource:
            An instance of a Django model that represents the resource this token is associated with.
        :param user:
            A :class:`~django.contrib.auth.models.User` to associate this access token with.
        :return:
            An :class:`~tokenauth.models.AccessToken` instance.

        """
        ct = ContentType.objects.get_for_model(resource)
        object_id = resource.pk
        token, created = self.model.objects.get_or_create(_content_type=ct, _object_id=object_id, user=user)

        if not created:
            if not token.expired:
                # todo: better logging
                print unicode.format(u"{0} existed. Reusing.", token)
            else:
                token.delete()
                token = self.model(resource=resource, user=user)
                token.save()
                # todo: better logging
                print unicode.format(u"Generated token: {0}", token)
        return token

    def validate(self, access_token, resource_id):
        """
        Verifies that an access token is valid for a given resource. This method is also used to
        get :class:`~tokenauth.models.AccessToken` objects from a string representation.

        :param access_token: A string or unicode object representing an access token.
        :param resource_id: The ID of the resource being accessed.
        :return: A tuple of ``(is_valid, token)`` where ``is_valid`` is a boolean indicating whether the token
                 provided is valid, and ``token`` is the :class:`~tokenauth.models.AccessToken` instance.

        """
        try:
            token = self.model.objects.get(token=access_token)
        except self.model.DoesNotExist:
            # access token doesn't exist
            return False, None

        # first check if the token is expired
        if token.expired:
            return False, None

        # check that the access token provided gives access to the resource requested
        if hasattr(token.resource, 'resource_id'):
            rid = token.resource.resource_id
        else:
            rid = token.resource.pk
        if resource_id != rid:
            return False, None

        # access token appears to be valid
        return True, token
