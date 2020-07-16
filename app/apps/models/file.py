# -*- coding:utf-8 -*-
"""
文件存储模型
"""

from flask import current_app
from mongoengine import *
from apps import db


class File(db.DynamicDocument):
    path = StringField()  # 路径
    name = StringField()
    extension = StringField()  # 后缀
    size = IntField()
    md5 = StringField()  # 图片md5值，防止上传重复图片

    @staticmethod
    def create_file(**kwargs):
        file = File()
        for key in kwargs.keys():
            if hasattr(file, key):
                setattr(file, key, kwargs[key])
        file.save()
        return file
        # return True
