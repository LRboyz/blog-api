# _*_ coding: utf-8 _*_
"""
  Created by 刘锐 on 2020/5/10.
  各种提交表单的验证
"""
import time

from flask import request
from wtforms import StringField, IntegerField, PasswordField, DateTimeField, \
    BooleanField, FieldList, FormField, Field
from wtforms.validators import DataRequired, length, Regexp, EqualTo, Optional

from apps.validaters.base import BaseForm as Form


# 注册校验
class RegisterForm(Form):
    nickname = StringField()
    password = PasswordField('新密码', validators=[
        DataRequired(message='新密码不可为空'),
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$', message='密码长度必须在6~22位之间，包含字符、数字和 _ '),
        EqualTo('confirm_password', message='两次输入的密码不一致，请输入相同的密码')])
    confirm_password = PasswordField('确认新密码', validators=[DataRequired(message='请确认密码')])
    username = StringField(validators=[DataRequired(message='用户名不可为空')])
    email = StringField('电子邮件', validators=[
        Regexp(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$',
               message='电子邮箱不符合规范，请输入正确的邮箱'),
        Optional()
    ])

    def get_errors(self):
        errors = ''
        for v in self.errors.values():
            for m in v:
                errors += m
            errors += '\n'
        return errors


# Token
class TokenForm(Form):
    token = StringField(validators=[DataRequired()])


# 登陆校验
class LoginForm(Form):
    username = StringField(validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired(message='密码不可为空')])


class CreateArticleForm(Form):
    title = StringField(validators=[DataRequired(message='必须输入文章标题')])
    content = StringField(validators=[DataRequired(message='必须传入文章内容')])
    article_type = IntegerField(validators=[])
    author = StringField(validators=[])
    tags = FieldList(StringField())
    keyword = StringField()
    source = StringField()
    commentsCount = IntegerField(validators=[])
    category = Field()
    introduction = StringField(validators=[])
    banner = StringField(validators=[])
    is_audit = BooleanField(validators=[])
    recommend = BooleanField(validators=[])


class CreateOrUpdateBookForm(Form):
    title = StringField(validators=[DataRequired(message='必须传入图书名')])
    author = StringField(validators=[DataRequired(message='必须传入图书作者')])
    summary = StringField(validators=[DataRequired(message='必须传入图书综述')])
    image = StringField(validators=[DataRequired(message='必须传入图书插图')])


# 用户头像
class AvatarUpdateForm(Form):
    avatar = StringField('头像', validators=[
        DataRequired(message='请输入头像url')
    ])


# 重置密码校验
class ResetPasswordForm(Form):
    new_password = PasswordField('新密码', validators=[
        DataRequired(message='新密码不可为空'),
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$', message='密码长度必须在6~22位之间，包含字符、数字和 _ '),
        EqualTo('confirm_password', message='两次输入的密码不一致，请输入相同的密码')
    ])
    confirm_password = PasswordField('确认新密码', validators=[DataRequired(message='请确认密码')])


# 更改密码校验
class ChangePasswordForm(ResetPasswordForm):
    old_password = PasswordField('原密码', validators=[DataRequired(message='不可为空')])


# 更新用户邮箱和昵称
class UpdateInfoForm(Form):
    email = StringField('电子邮件', validators=[
        Regexp(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', message='电子邮箱不符合规范，请输入正确的邮箱'),
        Optional()
    ])
    nickname = StringField(validators=[
        length(min=2, max=10, message='昵称长度必须在2~10之间'),
        Optional()
    ])


# 管理员的更新用户邮箱和昵称
class AdminUpdateInfoForm(Form):
    email = StringField('电子邮件', validators=[
        Regexp(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', message='电子邮箱不符合规范，请输入正确的邮箱'),
        Optional()
    ])
    role = IntegerField(validators=[])
    username = StringField(validators=[
        length(min=2, max=100, message='昵称长度必须在2~100之间'),
        Optional()
    ])


# 更新用户信息
class UpdateUserInfoForm(Form):
    email = StringField('电子邮件', validators=[
        Regexp(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', message='电子邮箱不符合规范，请输入正确的邮箱'),
        Optional()
    ])


# 日志查找范围校验
class LogFindForm(Form):
    # name可选，若无则表示全部
    name = StringField(validators=[Optional()])
    # 2020-05-03 09:39:35
    start = DateTimeField(validators=[])
    end = DateTimeField(validators=[])

    def validate_start(self, value):
        if value.data:
            try:
                _ = time.strptime(value.data, '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                raise e

    def validate_end(self, value):
        if value.data:
            try:
                _ = time.strptime(value.data, '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                raise e


class CreateTagForm(Form):
    tag_name = StringField(validators=[DataRequired(message='必须传入标签名称')])
    # remark = StringField(validators=[])
    status = BooleanField()
    thumbnail = StringField(120)


class CreateCategoryForm(Form):
    parent_category_name = StringField()
    category_name = StringField(validators=[DataRequired(message='必须传入标签名称')])
    thumbnail = StringField(120)


class CreateCommentForm(Form):
    text = StringField(validators=[DataRequired(message='必须传入评论内容')])
    # user_id = StringField()
    parent_id = StringField()
    post_id = StringField()
    # comment_user_id = StringField(validators=[DataRequired(message='必须传入评论人id')])
    reply_user_id = StringField()


class UpdateComment(Form):
    comment_id = StringField()
    status = BooleanField()
    text = StringField()

# class DeleteComment(Form):
#     comment_id = StringField()