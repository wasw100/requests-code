# -*- coding: utf-8 -*-
import os.path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'you need modify this into local_settings.py'

DEBUG = False
WTF_CSRF_ENABLED = False

BOOTSTRAP_SERVE_LOCAL = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'code.db')
SQLALCHEMY_ECHO = False
