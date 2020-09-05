"""
  Created by 刘锐 on 2020/4/24.
"""
__author__ = '刘锐'

from datetime import timedelta


class BaseConfig(object):
    """ 基础配置 """
    # 分页配置
    COUNT_DEFAULT = 10  # 默认返回数量
    PAGE_DEFAULT = 0  # 默认页数
    pass


class DevelopmentConfig(BaseConfig):
    """ 开发环境配置 """
    DEBUG = False
    # Token 配置
    # 令牌配置
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2400)
    # 数据库配置
    MONGODB_DB = 'blog'
    MONGODB_HOST = 'localhost'
    MONGODB_POST = '27017'
    MONGODB_USERNAME = None
    MONGODB_PASSWORD = None
    # 七牛云存储相关配置
    # 七牛云存储地址
    SITE_DOMAIN = 'http://www.lrboy.live/'
    # 文件相关配置
    FILE = {
        "STORE_DIR": 'apps/static',
        "SINGLE_LIMIT": 1024 * 1024 * 2,
        "TOTAL_LIMIT": 1024 * 1024 * 20,
        "NUMS": 10,
        "INCLUDE": set([]),
        "EXCLUDE": set([])
    }

    access_key = 'NgP597T5QzNUhCygvVIYFngUs7bzheOFtHGDtz-u'
    secret_key = 'mV7iHCAft8az-X3nE7x3gxOw1vbavFjkLEWUEGLF'

    # 所有endpoint的meta信息
    EP_META = {}
    EP_INFO_LIST = []
    EP_INFOS = {}


class ProductionConfig(BaseConfig):
    """ 生产环境配置 """
    DEBUG = False
    # Token 配置
    # 令牌配置
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    # 数据库配置
    MONGODB_DB = 'blog'
    MONGODB_HOST = '172.17.40.142'
    MONGODB_POST = '27017'
    MONGODB_USERNAME = None
    MONGODB_PASSWORD = None
    # 七牛云存储相关配置
    # 七牛云存储地址
    SITE_DOMAIN = 'http://www.lrboy.live/'
    # 文件相关配置
    FILE = {
        "STORE_DIR": 'apps/static',
        "SINGLE_LIMIT": 1024 * 1024 * 2,
        "TOTAL_LIMIT": 1024 * 1024 * 20,
        "NUMS": 10,
        "INCLUDE": set([]),
        "EXCLUDE": set([])
    }

    access_key = 'NgP597T5QzNUhCygvVIYFngUs7bzheOFtHGDtz-u'
    secret_key = 'mV7iHCAft8az-X3nE7x3gxOw1vbavFjkLEWUEGLF'

    # 所有endpoint的meta信息
    EP_META = {}
    EP_INFO_LIST = []
    EP_INFOS = {}
