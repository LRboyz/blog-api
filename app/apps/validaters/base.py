# _*_ coding: utf-8 _*_
"""
  Created by 刘锐 on 2020/5/11.
"""

__author__ = '刘锐'

from flask import request
from wtforms import Form as WTForm

from apps.core.error import ParameterException


class BaseForm(WTForm):
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        # print(valid) False
        if not valid:
            msg = self.get_errors()
            raise ParameterException(msg=msg)
        return self

    def get_errors(self):
        errors = ''
        for v in self.errors.values():
            for m in v:
                errors += m
            errors += '\n'
        return errors
