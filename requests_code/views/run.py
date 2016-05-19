# -*- coding: utf-8 -*-
import sys
import subprocess
from flask import Blueprint, render_template, make_response, jsonify
from flask.views import MethodView

from requests_code.models import Code
from requests_code.forms import CodeForm

bp = Blueprint('run', __name__)

EXEC = sys.executable


class RunView(MethodView):

    def get(self, filename):
        """如果文件存在, 从本地读取代码返回到界面"""
        if filename:
            obj = Code.get_by_name(filename)
        else:
            obj = None

        if not obj:
            code = '# -*- coding: utf-8 -*-'
            form = CodeForm()
            form.code.data = code
        else:
            form = CodeForm(obj=obj)
            form.code.data = form.get_code()
        return render_template('code-page.html', form=form)

    def post(self, filename):
        """将文件保存到指定文件中, 并执行, 返回执行后的结果"""
        form = CodeForm()
        code = form.code.data
        action = form.action.data

        filename = form.get_name()
        if action == CodeForm.ACTION_EXEC:
            # 保存数据到数据库, 并保存文件到本地
            form.save()
            # 使用 subprocess.check_output 执行后, 返回执行结果
            try:
                filepath = form.get_filepath()
                output = subprocess.check_output(
                    [EXEC, filepath],
                    stderr=subprocess.STDOUT,
                    timeout=10
                )
                r = dict(
                    name=form.get_name(),
                    output=output.decode()
                )
            except subprocess.CalledProcessError as e:
                r = dict(error='Exception', output=e.output)
            except subprocess.TimeoutExpired as e:
                r = dict(error='Timeout', output='执行超时')
            except subprocess.CalledProcessError as e:
                r = dict(error='Error', output='执行错误')
            return jsonify(r)
        else:
            resp = make_response(code)
            resp.mimetype = 'text/plain'
            resp.headers['Content-Disposition'] = \
                'attachment; filename={0}'.formate(filename)
            return resp


view_func = RunView.as_view('run')
bp.add_url_rule('/run', defaults={'filename': None},
                view_func=view_func)
bp.add_url_rule('/run/<filename>', view_func=view_func)
