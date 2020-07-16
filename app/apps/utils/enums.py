# _*_ coding: utf-8 _*_
"""
  Created by LiuRui on 2020/5/11.
"""
from enum import Enum


class ScopeEnum(Enum):
    """"
    用法：ScopeEnum(1) == ScopeEnum.COMMON # True
    """
    COMMON = 1  # 普通用户
    ADMIN = 2  # 管理员


