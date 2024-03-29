# -*- coding:utf-8 -*-
import datetime
from time import time
from hashlib import md5

from bson import ObjectId
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_current_user, verify_jwt_refresh_token_in_request, get_jwt_identity, \
    create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash
from apps.core.error import RepeatException, Success, ParameterException, RefreshException, NotFound, Failed
from apps.core.token_auth import get_tokens, login_required
from apps.models.category import Category
from apps.models.log import Log
from apps.models.permissions import append_permission
from apps.models.article import Article
from apps.models.tag import Tag
from apps.models.user import User
from apps.utils.api_format import api_exclude
from apps.utils.logger import Logger
from apps.validaters.forms import RegisterForm, LoginForm, UpdateInfoForm, AvatarUpdateForm, ChangePasswordForm

user_api = Blueprint('user', __name__)


@user_api.route('/register', methods=['POST'])
# @Logger(template='{user.username}创建了一个用户')
def register():
    form = RegisterForm().validate_for_api()
    user = User.objects(username=form.username.data).first()
    if user:
        raise RepeatException(msg='该账户名已被注册，请重新输入')
    if form.email.data and form.email.data.strip() != "":
        email = User.objects(email=form.email.data).first()
        if email:
            raise RepeatException(msg='该邮箱已被注册，请重新输入')
    _register_user(form)
    return Success(msg="用户创建成功!", code=200)


@user_api.route('/token', methods=['POST'])
def get_token():
    form = LoginForm().validate_for_api()
    user_id = User.verify(form.username.data, form.password.data)
    access_token, refresh_token = get_tokens(user_id)
    User.objects(id=ObjectId(user_id['uid'])).update(last_login=datetime.datetime.now())  # 记录最后登陆时间
    return jsonify(access_token=access_token, refresh_token=refresh_token), 201


@user_api.route('/refresh', methods=['GET'])
def refresh():
    try:
        verify_jwt_refresh_token_in_request()
    except Exception:
        return RefreshException()

    identity = get_jwt_identity()
    if identity:
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        return jsonify(access_token=access_token, refresh_token=refresh_token)
    return NotFound(msg='refresh_token未被识别')


@user_api.route('/permissions', methods=['GET'])
@login_required
def get_info():
    user = get_current_user()
    user_info = User.objects(id=user.id).first()
    user_info['permissions'] = append_permission(user.role)
    user_info['is_superuser'] = True if user.role == 300 else False
    data = User.to_dict(user_info)
    article_count = Article.objects.count()
    category_count = Category.objects.count()
    tag_count = Tag.objects.count()
    data['article_count'] = article_count
    data['category_count'] = category_count
    data['tag_count'] = tag_count
    Log.create_log(
        message=f'{user.username}登陆成功获取了令牌',
        user_id=str(user.id), user_name=user.username, create_time=int(time()*1000),
        status_code=200, method=request.method, path=request.path, ip_addr=request.remote_addr
    )
    return jsonify(data)


@user_api.route('/update', methods=['PUT'])
@login_required
def update_user():
    form = UpdateInfoForm().validate_for_api()
    user = get_current_user()
    user = User.objects(id=user.id).first()
    if user.nickname is None:
        user.nickname = form.nickname.data
        user.save()
    else:
        user.update(set__nickname=form.nickname.data)
    return Success(msg='操作成功')


@user_api.route('/avatar', methods=['PUT'])
@login_required
def set_avatar():
    form = AvatarUpdateForm().validate_for_api()
    user_info = get_current_user()
    user = User.objects(id=user_info.id).first()
    if user.avatar is None:
        user.avatar = form.avatar.data
        user.save()
    else:
        user.update(set__avatar=form.avatar.data)
    return Success(msg='更新头像成功')


@user_api.route('/information', methods=['GET'])
@login_required
def get_information():
    current_user = get_current_user()  # <class 'apps.models.user.User'>
    user_info = api_exclude(current_user, '_password')
    return jsonify(user_info)


@user_api.route('/change_password', methods=['PUT'])
@Logger(template='{user.username}修改了自己的密码')  # 记录日志
@login_required
def change_password():
    form = ChangePasswordForm().validate_for_api()
    user = get_current_user()
    success = user.change_password(user.id, form.old_password.data, form.new_password.data)
    if success:
        return Success(msg='密码修改成功')
    else:
        return Failed(msg='修改密码失败！')


def _register_user(form: RegisterForm):
    user = User()
    user.username = form.username.data
    if form.email.data and form.email.data.strip() != "":
        user.email = form.email.data
    user._password = generate_password_hash(form.password.data)
    user.ip = user.get_ip()
    user.nickname = form.nickname.data
    avatar_hash = md5(user.username.encode('utf-8')).hexdigest()
    user.avatar = 'https://www.gravatar.com/avatar/%s?d=monsterid' % avatar_hash  # 生成随机小怪兽头像
    user.save()
    return True
