# -*- coding:utf-8 -*-
"""
系统初始化架构
"""
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_cors import CORS


db = MongoEngine()


def apply_cors(app):
    CORS(app)


def apply_json_encoder(app):
    from apps.core.json_encoder import JSONEncoder
    app.json_encoder = JSONEncoder


def register_blueprints(app):
    """
    加载蓝图 apps.register_blueprint(user, url_prefix='/user')    # 注册user蓝图，并指定前缀。
    """
    # CMS管理系统模块API
    from apps.views.cms.test import test
    from apps.views.cms.book import book_api
    from apps.views.cms.user import user_api
    from apps.views.cms.log import log_api
    from apps.views.cms.file import file_api
    from apps.views.cms.tag import tag_api
    from apps.views.cms.post import post_api
    from apps.views.cms.category import cat_api
    from apps.views.cms.admin import admin_api
    from apps.views.cms.comment import cms_comment_api

    # 博客前端模块API
    from apps.views.blog.index import blog_api
    from apps.views.blog.articleDetail import article_api
    from apps.views.blog.comment import comment_api

    app.register_blueprint(test, url_prefix='/test')
    app.register_blueprint(user_api, url_prefix='/user')
    app.register_blueprint(log_api, url_prefix='/v1')
    app.register_blueprint(file_api, url_prefix='/v1')
    app.register_blueprint(book_api, url_prefix='/book')
    app.register_blueprint(tag_api, url_prefix='/tag')
    app.register_blueprint(post_api, url_prefix='/post')
    app.register_blueprint(cat_api, url_prefix='/category')
    app.register_blueprint(admin_api, url_prefix='/admin')
    app.register_blueprint(cms_comment_api, url_prefix='/cms/comment')

    app.register_blueprint(blog_api, url_prefix='/blog')
    app.register_blueprint(article_api, url_prefix='/article')
    app.register_blueprint(comment_api, url_prefix='/blog/comment')


def create_app(environment='development'):
    """  系统初始化
    服务器环境使用product.cfg，开发者严禁在项目中创建此文件
    开发使用 apps/config.cfg ( 项目中的apps/config.ini 是范例文件 )
    """

    # 初始化 Flask Application
    app = Flask(__name__)
    app.config['ENV'] = environment
    env = app.config.get('ENV')
    if env == 'production':
        app.config.from_object('apps.config.setting.ProductionConfig')
        app.config.from_object('apps.config.secure.ProductionSecure')
    elif env == 'development':
        app.config.from_object('apps.config.setting.DevelopmentConfig')
        app.config.from_object('apps.config.secure.DevelopmentSecure')
    # app.config.from_object('apps.config.setting')
    db.init_app(app)
    # JSON序列化
    apply_json_encoder(app)
    # 注册蓝图
    register_blueprints(app)
    # 跨域
    apply_cors(app)
    # 加载jwt插件
    from apps.core.token_auth import jwt
    jwt.init_app(app)
    return app
