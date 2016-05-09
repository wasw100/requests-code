# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for, jsonify
from flask.views import MethodView

from requests_code import utils
from requests_code.database import db
from requests_code.models import Code


bp = Blueprint('code', __name__)


def IndexView(MethodView):
    def get(self):
        return redirect(url_for('.list'))


class ItemView(MethodView):
    def delete(self, item_id):
        item = Code.query.get_or_404(item_id)
        utils.delete_code(item.name)
        db.session.delete(item)
        db.session.commit()
        return jsonify(errcode=0, errmsg='')


class ListView(MethodView):

    def get(self):
        """列表页"""
        items = Code.query.order_by(Code.id.desc()).all()
        return render_template('list.html', items=items)

bp.add_url_rule('/', view_func=ListView.as_view('home'))
bp.add_url_rule('/list', view_func=ListView.as_view('list'))
bp.add_url_rule('/code/<int:item_id>', view_func=ItemView.as_view('item'))
