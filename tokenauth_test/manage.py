#!/usr/bin/env python
# coding=utf-8
import os
import sys
from path import path
from propane.importing import add_to_path_if_needed

p = path(__file__).abspath().dirname().dirname()

if __name__ == "__main__":
    add_to_path_if_needed(p)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tokenauth_test.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
