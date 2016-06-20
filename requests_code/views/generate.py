# -*- coding: utf-8 -*-
"""生成代码的views"""
import json


from flask import Blueprint, render_template, make_response, redirect, url_for
from flask.views import MethodView

from requests.compat import urljoin, urlsplit
from requests.structures import CaseInsensitiveDict

from requests_code.forms import RequestDataForm, CodeForm

try:
    from urllib.parse import parse_qsl
except ImportError:
    from urlparse import parse_qsl

try:
    from http.cookies import SimpleCookie
except ImportError:
    from Cookie import SimpleCookie

bp = Blueprint('generate', __name__)


def repr_value(value):
    if isinstance(value, (str, bytes)) and value.isdigit():
        return value
    return repr(value)


class IndexView(MethodView):

    def get(self):
        from flask import current_app
        form = RequestDataForm()
        return render_template('generate.html', form=form)

    def post(self):
        form = RequestDataForm()
        data = form.data.data.lstrip()
        lines = data.splitlines(True)
        if len(lines) < 3:
            return 'data less 3 lines'

        origin_headers = []
        body = []
        body_start = False

        for index, line in enumerate(lines):
            if index == 0:
                method, path, _ = line.split(' ')
                continue

            if not line.split():
                body_start = True
                continue

            if body_start:
                body.append(line)
            else:
                line = line.strip()
                key, value = line.split(': ', 1)
                origin_headers.append((key, value))

        # for get header value
        header_dict = CaseInsensitiveDict(origin_headers)

        method = method.lower()
        body = ''.join(body)
        content_type = header_dict.get('Content-Type', '')

        # set headers
        headers = []
        origin_host = header_dict.get('Host')
        if form.host.data and origin_host and form.host.data != origin_host:
            headers.append(('Host', header_dict.get('Host')))
        user_agent = header_dict.get('User-Agent')
        referer = header_dict.get('Referer')
        if user_agent:
            headers.append(('User-Agent', user_agent))
        if referer:
            headers.append(('Referer', referer))

        # set cookie
        cookies = []
        cookie = header_dict.get('Cookie')
        C = SimpleCookie(cookie)
        for morsel in C.values():
            cookies.append((morsel.key, morsel.coded_value))

        host = form.host.data or header_dict.get('Host')
        p = urlsplit(path)
        url = urljoin('http://{}'.format(host), p.path)
        params = [(x, repr_value(y)) for x, y in parse_qsl(p.query)]

        if method == 'get' or not content_type:
            pass
        elif 'x-www-form-urlencoded' in content_type:
            body = [(x, repr_value(y)) for x, y in parse_qsl(body)]
        elif 'json' in content_type:
            body = [(x, repr_value(y)) for x, y in json.loads(body).items()]
        else:
            headers.append(('Content-Type', content_type))

        code = render_template(
            'code.html',
            method=method,
            url=url,
            params=params,
            body=body,
            headers=headers if form.contain_headers.data else None,
            cookies=cookies if form.contain_cookies.data else None,
            content_type=content_type
        )
        code_form = CodeForm()
        code_form.code.data = code
        code_form.name.data = form.filename.data
        code_form.desc.data = form.desc.data
        name = code_form.save()
        url = url_for('run.run', filename=name)
        return redirect(url)


class CodeView(MethodView):

    def post(self):
        form = CodeForm()
        action = form.action.data
        code = form.code.data
        if action == CodeForm.ACTION_EXEC:
            global_env = globals()
            local_env = globals()
            exec(code, global_env, local_env)
            result = main()     # noqa
            resp = make_response(result)
            resp.mimetype = 'text/plain'
            return resp
        else:
            resp = make_response(code)
            resp.mimetype = 'text/plain'
            resp.headers['Content-Disposition'] = \
                'attachment; filename=main.py'
            return resp


bp.add_url_rule('/generate', view_func=IndexView.as_view('index'))
# bp.add_url_rule('/code', view_func=CodeView.as_view('code'))
