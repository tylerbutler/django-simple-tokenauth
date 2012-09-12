# coding=utf-8

import sys

from datetime import timedelta
import uuid
from django.test import TestCase
from django.utils import timezone
from django_any.contrib import any_user, any_model_with_defaults
from django_any.models import any_model
from tokenauth.models import AccessToken, AccessTokenManager
from tokenauth_test.models import SimpleResource

class AccessTokenTest(TestCase):
    fixtures = ['resources.json']

    def setUp(self):
        self.resource = any_model(SimpleResource)

        # pass specific datetimes to any_user because it's not yet timezone-aware - works around RuntimeWarnings
        self.user = any_user(date_joined=timezone.now(), last_login=timezone.now())

    def test_create(self):
        token = AccessToken.create_token(self.resource, self.user)
        self.assertEqual(token.user, self.user)
        self.assertEqual(AccessToken.objects.all().count(), 1)

    def test_valid(self):
        token_str = unicode(AccessToken.create_token(self.resource, self.user))
        valid, token = AccessToken.validate(token_str, self.resource.pk)
        self.assertTrue(valid)
        self.assertEqual(token.token, token_str)

    def test_wrong_resource(self):
        token_str = unicode(AccessToken.create_token(self.resource, self.user))
        new_resource = any_model(SimpleResource)
        valid, token = AccessToken.validate(token_str, new_resource.pk)
        self.assertFalse(valid)

    def test_bad_token(self):
        token = uuid.uuid4()
        valid, token = AccessToken.validate(token, self.resource.pk)
        self.assertFalse(valid)

    def test_expiration(self):
        token = AccessToken.create_token(self.resource, self.user)
        token.time_issued = timezone.now() - timedelta(hours=2)
        token.save()
        valid, token = AccessToken.validate(token, self.resource.pk)
        self.assertFalse(valid)

    def test_expiration_recreation(self):
        token = AccessToken.create_token(self.resource, self.user)
        token.time_issued = timezone.now() - timedelta(hours=2)
        token.save()
        self.assertTrue(token.expired)
        valid, token = AccessToken.validate(token, self.resource.pk)
        self.assertFalse(valid)

        new_token = AccessToken.create_token(self.resource, self.user)
        self.assertFalse(new_token.expired)
        valid, new_token = AccessToken.validate(new_token, self.resource.pk)
        self.assertTrue(valid)
