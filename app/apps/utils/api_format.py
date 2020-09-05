# -*- coding: utf-8 -*-
"""
定义API返回格式与规范

"""


# 序列化处理，排除指定字段
def api_exclude(obj, *args):
    model_dict = obj.to_mongo().to_dict()
    if args:
        list(map(model_dict.pop, list(args)))
    if "_id" in model_dict.keys():
        model_dict["_id"] = str(model_dict["_id"])
    return model_dict


# 序列化处理，只返回特定字段
def api_fields(obj, *args):
    model_dict = obj.to_mongo().to_dict()
    if args:
        fields = [i for i in model_dict.keys() if i not in list(args)]
        list(map(model_dict.pop, fields))
    if "_id" in model_dict.keys():
        model_dict["_id"] = str(model_dict["_id"])
    return model_dict


def success_ret(msg='', data=None, code=200, **kwargs):
    """
    请求成功时返回API结构
    :return:
    """
    return {
        'code': code,
        'msg': msg,
        'data': {} if data is None else data,
        **kwargs,
    }


def error_ret(code, msg='', data=None, **kwargs):
    """
    请求错误时返回API结构
    :return:
    """
    return {
        'code': code,
        'msg': msg,
        'data': data if data else {},
        **kwargs
    }
