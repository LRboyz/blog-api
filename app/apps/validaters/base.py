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
        if not valid:
            raise ParameterException(msg=self.errors)
        return self
