# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Link

from requests_code import config as _config
from requests_code.views import bp


nav = Nav()

nav.register_element('top', Navbar(
    View('Home', 'home.index'),
    Link('使用说明', 'http://www.baidu.com/'),
))


def create_app(config=None):
    app = Flask(__name__)
    if config is not None:
        app.config.from_pyfile(config)
    else:
        app.config.from_object(_config)

    app.jinja_env.autoescape = False

    Bootstrap(app)
    nav.init_app(app)
    app.register_blueprint(bp)

    return app
