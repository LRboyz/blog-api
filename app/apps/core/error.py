# _*_ coding: utf-8 _*_
"""
  Created by 刘锐 on 2020/5/1.
"""
from flask import request, json
from flask import jsonify
from werkzeug.exceptions import HTTPException

__author__ = '刘锐'


class APIException(HTTPException):
    code = 500  # http 状态码
    msg = '服务器未知错误'  # 异常信息
    res_code = 999  # 约定的异常码

    def __init__(self, code=None, res_code=None, msg=None, headers=None):
        if code:
            self.code = code
        if res_code:
            self.res_code = res_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__()

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            res_code=self.res_code,
            request_url=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)  # 返回文本
        return text

    def get_headers(self, environ=None):
        return [('Content-type', 'application/json; charset=utf-8')]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')[0]
        return main_path


############################################
#    基础类错误(0~9999)   ##########
############################################
class Success(APIException):
    code = 200
    res_code = 200
    msg = '成功'


class ServerError(APIException):
    code = 500
    res_code = 999
    msg = '服务器端异常'


class Forbidden(APIException):
    code = 401
    msg = '不可操作'
    res_code = 10070


class Failed(APIException):
    code = 400
    res_code = 9999
    msg = '失败'


############################################
# 基础类错误(11000~12000) ##########
############################################
#  权限相关(10000~10100)  ##########

class AuthFailed(APIException):
    code = 401
    msg = '认证失败'
    res_code = 10000


class NotFound(APIException):
    code = 404
    msg = '资源不存在'
    res_code = 10020


class ParameterException(APIException):
    code = 400
    msg = '参数错误'
    res_code = 10030


class PasswordException(APIException):
    code = 402
    msg = '密码校验错误'
    res_code = 10031


class InvalidTokenException(APIException):
    code = 401
    msg = '令牌失效'
    res_code = 10040


class ExpiredTokenException(APIException):
    code = 422
    msg = '令牌过期'
    res_code = 10050


class RefreshException(APIException):
    code = 401
    msg = "refresh token 获取失败"
    res_code = 10100


class UnknownException(APIException):
    code = 500
    msg = '服务器未知错误'
    res_code = 999


class RepeatException(APIException):
    code = 400
    msg = '字段重复'
    res_code = 10060


class Forbidden(APIException):
    code = 401
    msg = '不可操作'
    res_code = 10070


class RefreshException(APIException):
    code = 401
    msg = 'refresh token 获取失败'
    res_code = 10100


class FileTooLargeException(APIException):
    code = 413
    msg = '文件体积过大'
    res_code = 10110


class FileTooManyException(APIException):
    code = 413
    msg = '文件数量过多'
    res_code = 10120


class FileExtensionException(APIException):
    code = 401
    msg = '文件扩展名不符合规范'
    res_code = 10130


