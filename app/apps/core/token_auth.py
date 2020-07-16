# _*_ coding: utf-8 _*_
"""
  Created by 刘锐 on 2020/5/06.
"""


from flask import request
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_current_user,\
    create_access_token, create_refresh_token
from functools import wraps
from apps.core.error import AuthFailed, InvalidTokenException, ExpiredTokenException, NotFound
from apps.models.user import User

jwt = JWTManager()
identity = dict(uid=0)


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_current_user()
        # print(current_user, current_user.role) # token  0
        if current_user.role != 300:  # 暂且先这样吧 - -！，没想到什么好的方案 (JWT有效且是管理员)
            raise AuthFailed(msg='只有超级管理员可操作')
        return fn(*args, **kwargs)

    return wrapper


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return fn(*args, **kwargs)
    return wrapper


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    if 'remote_addr' in identity.keys() and identity['remote_addr'] != request.remote_addr:
        raise AuthFailed()
    # token is granted , user must be exit
    # 如果token已经被颁发，则该用户一定存在
    user = User.objects(id=identity['uid']).first()
    if user is None:
        raise NotFound(msg='用户不存在')
    return user


@jwt.expired_token_loader
def expired_loader_callback():
    return ExpiredTokenException()


@jwt.invalid_token_loader
def invalid_loader_callback(e):
    return InvalidTokenException()


@jwt.unauthorized_loader
def unauthorized_loader_callback(e):
    return AuthFailed(msg='认证失败，请检查请求头或者重新登陆')


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        'uid': identity['uid'],
        'remote_addr': identity['remote_addr'] if
        'remote_addr' in identity.keys() else None
    }


def get_tokens(user, verify_remote_addr=False):
    identity['uid'] = user['uid']
    if verify_remote_addr:
        identity['remote_addr'] = request.remote_addr
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    return access_token, refresh_token


def get_access_token(user, fresh=False, expires_delta=None, verify_remote_addr=False):
    identity['uid'] = user.uid
    if verify_remote_addr:
        identity['remote_addr'] = request.remote_addr
    access_token = create_access_token(
        identity=identity,
        fresh=fresh,
        expires_delta=expires_delta,
    )
    return access_token


def get_refresh_token(user,  expires_delta=None, verify_remote_addr=False):
    identity['uid'] = user.uid
    if verify_remote_addr:
        identity['remote_addr'] = request.remote_addr
    refresh_token = create_refresh_token(
        identity=identity,
        expires_delta=expires_delta
    )
    return refresh_token


def verify_access_token():
    __verify_token('access')


def verify_refresh_token():
    __verify_token('refresh')


def __verify_token(request_type):
    from flask import request
    from flask_jwt_extended.config import config
    from flask_jwt_extended.view_decorators import _decode_jwt_from_cookies as decode
    from flask_jwt_extended.utils import verify_token_claims
    try:
        from flask import _app_ctx_stack as ctx_stack
    except ImportError:
        from flask import _request_ctx_stack as ctx_stack

    if request.method not in config.exempt_methods:
        jwt_data = decode(request_type=request_type)
        ctx_stack.top.jwt = jwt_data
        verify_token_claims(jwt_data)


# def _check_is_active(current_user):
#     if not current_user.is_active:
#         raise AuthFailed(msg='您目前处于未激活状态，请联系超级管理员')
