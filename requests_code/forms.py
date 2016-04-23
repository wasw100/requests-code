# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask_wtf import Form
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import Optional, Required


class RequestDataForm(Form):
    host = StringField('Host', [Optional()])
    data = TextAreaField('Request raw', [Required()])
    action = StringField('action', [Required()])


class CodeForm(Form):
    code = TextAreaField(u'代码')
    action = StringField('action')

    ACTION_EXEC = 'exec'
    ACTION_DOWNLOAD = 'download'
