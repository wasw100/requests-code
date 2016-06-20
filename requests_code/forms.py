# -*- coding: utf-8 -*-
import os.path
import string
from flask import current_app
from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import Optional, Required

from requests_code.database import db
from requests_code.models import Code


class RequestDataForm(Form):
    host = StringField(
        u'Host', [Optional()],
        render_kw={'placeholder': u'不需要填写, 如果访问指定服务器填写IP或域名'}
    )
    filename = StringField(
        '', [Optional()],
        render_kw={'placeholder': u'文件名, 例如user.py, 不填会自动生成'}
    )
    desc = StringField(
        '', [Optional()],
        render_kw={'placeholder': u'描述, 选填'}
    )
    contain_headers = BooleanField(u'包含User-Agent', default=False)
    contain_cookies = BooleanField(u'包含cookie', default=True)
    data = TextAreaField(
        '', [Required()],
        render_kw={'rows': 16, 'placeholder': u'抓包的数据'}
    )
    submit = SubmitField(u'生成代码')


class CodeForm(Form):
    name = StringField('名字', [Optional()])
    desc = StringField('描述', [Optional()])
    code = TextAreaField(u'代码')
    action = StringField('action')

    ACTION_EXEC = 'exec'
    ACTION_DOWNLOAD = 'download'

    @staticmethod
    def generate_name():
        """获取唯一的文件名"""
        name_id = (Code.get_max_id() or 0) + 1
        name = '{0}.py'.format(name_id)
        if not Code.get_by_name(name):
            return name
        for c in string.letters:
            name = '{0}{1}.py'.format(c, name_id)
            if not Code.get_by_name(name):
                return name

    def get_name(self):
        name = self.name.data
        if name:
            if not name.endswith('.py'):
                name += '.py'
        else:
            name = self.generate_name()
        self.name.data = name
        return name

    def get_filepath(self, name=None):
        name = name or self.get_name()
        return os.path.join(current_app.base_dir,
                            'code/{}'.format(self.get_name()))

    def get_code(self):
        filepath = self.get_filepath()
        with open(filepath, 'r') as f:
            return f.read()

    def save(self):
        name = self.get_name()
        filepath = self.get_filepath(name)
        with open(filepath, 'w') as f:
            f.write(self.code.data)

        code = Code.get_by_name(name)
        if not code:
            code = Code(name=name, desc=self.desc.data)
        else:
            code.desc = self.desc.data
        db.session.add(code)
        db.session.commit()
        return name
