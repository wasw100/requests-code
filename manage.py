# -*- coding: utf-8 -*-
from flask_script import Manager
from requests_code import create_app

manager = Manager(create_app)


if __name__ == '__main__':
    manager.run()
