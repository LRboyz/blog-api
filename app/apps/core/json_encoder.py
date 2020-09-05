# _*_ coding: utf-8 _*_
"""
  Created by 刘锐 on 2020/4/21.
"""
from flask import Flask as _Flask
from datetime import date
from flask.json import JSONEncoder as _JSONEncoder
from bson import ObjectId
from apps.core.error import ServerError

__author__ = '刘锐'


class JSONEncoder(_JSONEncoder):

    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(o, ObjectId):
            return str(o)
        # raise ServerError()


class Flask(_Flask):
    json_encoder = JSONEncoder
