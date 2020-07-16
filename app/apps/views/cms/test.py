# -*- coding:utf-8 -*-

from flask import Blueprint, jsonify

test = Blueprint('test', __name__)


@test.route('')
def test_api():
    return jsonify(code=200, msg='test API is Success!')



