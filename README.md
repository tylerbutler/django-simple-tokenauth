django-simple-tokenauth
=======================

The `tokenauth` app provides a set of models, decorators, and a custom authentication backend that can be used to
add simple token-based authentication to a Django project.

An access token has the following characteristics:

1. It is valid for a *single* user and resource combination.
2. It expires after a period of time automatically. By default this is two hours but it's configurable.

Brief Examples
--------------

### Creating an Access Token

    from tokenauth.models import AccessToken

    token = AccessToken.create_token(resource, user)

### Validating an Access Token

    is_valid, token = AccessToken.validate(access_token_as_string, resource_id)
    if is_valid:
        ... # do something
    else:
        ... # do something else

**More examples in the documentation.**
