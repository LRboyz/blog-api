import time

from mongoengine import *
from apps import db


class Log(db.DynamicDocument):
    # 日志模型
    message = StringField()
    # 日志时间
    create_time = IntField()
    # 引用字段
    user_id = StringField()
    # 用户当时的昵称
    user_name = StringField()
    # : 请求的http返回码
    status_code = IntField()
    # 请求方法
    method = StringField()
    # 请求路径
    path = StringField()
    # ip地址
    ip_addr = StringField()

    def to_dict(self):
        log_dict = self.to_mongo().to_dict()
        log_dict['user_id'] = log_dict['_id']
        return log_dict

    @staticmethod
    def create_log(**kwargs):
        log = Log()
        for key in kwargs.keys():
            if hasattr(log, key):
                setattr(log, key, kwargs[key])
        log.save()
        return log
