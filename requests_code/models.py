# -*- coding: utf-8 -*-
from datetime import datetime
from requests_code.database import db


class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    desc = db.Column(db.String(255))
    update_time = db.Column(db.DateTime)
    insert_time = db.Column(db.DateTime, default=datetime.now)

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_max_id(cls):
        max_id, = db.session.query(db.func.max(cls.id)).first()
        return max_id
