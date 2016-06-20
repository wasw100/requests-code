# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Link

import config as _config
from requests_code.database import db
from requests_code.views import generate, run, code


nav = Nav()

nav.register_element('top', Navbar(
    View('Home', 'code.home'),
    View('Generate Code', 'generate.index'),
    View('OJ', 'run.run'),
    View('List', 'code.list'),
    Link('使用说明', 'http://www.baidu.com/'),
))


def create_app(config=None):
    app = Flask(__name__)
    if config is not None:
        app.config.from_pyfile(config)
    else:
        app.config.from_object(_config)
    app.base_dir = app.config['BASE_DIR']

    app.jinja_env.autoescape = False

    db.init_app(app)

    Bootstrap(app)
    nav.init_app(app)

    # register blueprint
    for i in (generate, run, code):
        app.register_blueprint(i.bp)

    return app
