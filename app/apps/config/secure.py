"""
    :copyright: © 2020 by the LiuRui.
"""

# 安全性配置
from apps.config.setting import BaseConfig


class DevelopmentSecure(BaseConfig):
    """
    开发环境安全性配置
    """
    SECRET_KEY = '\x88W\xf09\x91\x07\x98\x89\x87\x96\xa0A\xc68\xf9\xecJJU\x17\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x95*4'


class ProductionSecure(BaseConfig):
    """
    生产环境安全性配置
    """
    SECRET_KEY = '\x88W\xf09\x91\x07\x98\x89\x87\x96\xa0A\xc68\xf9\xecJJU\x17\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x95*4'