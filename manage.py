# -*- coding: utf-8 -*-
from flask_script import Manager, Server
from requests_code import create_app
from requests_code.database import db

manager = Manager(create_app)


@manager.command
def init_db():
    # 只重新创建默认数据库的表
    db.drop_all(bind=None)
    db.create_all(bind=None)


manager.add_command('runserver', Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0')
)


if __name__ == '__main__':
    manager.run()
