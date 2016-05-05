# -*- coding: utf-8 -*-
from flask_script import Manager, Server
from requests_code import create_app

manager = Manager(create_app)

manager.add_command('runserver', Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0')
)


if __name__ == '__main__':
    manager.run()
