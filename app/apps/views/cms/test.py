# -*- coding:utf-8 -*-

from flask import Blueprint, jsonify
from hashlib import md5
from apps.core.token_auth import admin_required
from apps.validaters.forms import RegisterForm

test = Blueprint('test', __name__)


@test.route('')
# @admin_required
def test_api():
    a = 'https://www.gravatar.com/avatar/' + md5(b'603552916@qq.com').hexdigest()
    print(a)
    return jsonify(code=201, url=a)



