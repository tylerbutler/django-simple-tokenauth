from django.contrib.auth.models import User
from tokenauth.models import AccessToken

class AccessTokenAuthenticationBackend(object):
    """
    A Django authentication backend that authenticates a user based on an :class:`~tokenauth.models.AccessToken`.
    """
    supports_object_permissions = True
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, access_token, resource_id):
        valid, token = AccessToken.objects.validate(access_token, resource_id)
        if valid:
            return token.user
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

