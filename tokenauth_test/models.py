# coding=utf-8
from django.db import models

__author__ = 'Tyler Butler <tyler@tylerbutler.com>'

class SimpleResource(models.Model):
    value = models.IntegerField()
