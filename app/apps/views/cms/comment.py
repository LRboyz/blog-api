# -*- coding: utf-8 -*-
# @Time : 2020/11/22 8:24 下午
# @Author : LR
# @Site : 
# @File : comment.py
# @Software: PyCharm
from bson import ObjectId
from flask import Blueprint, jsonify, request
from apps.core.error import Success, RepeatException
from apps.core.token_auth import login_required
from apps.models.comment import Comment
from apps.utils import paginate
from apps.utils.api_format import success_ret, api_exclude
from apps.validaters.forms import UpdateComment

cms_comment_api = Blueprint('cms_comment', __name__)


@cms_comment_api.route('/list', methods=['GET'])
@login_required
def get_cms_comment_list():
    start, count = paginate()  # 获取分页配置
    print(start, count)
    result = Comment.objects.skip(start).limit(count).all()
    comment_list = [api_exclude(comment, '_cls') for comment in result]
    total = result.count()
    return success_ret(data=comment_list, total=total, msg='Get Cms CommentList Success！')


@cms_comment_api.route('/<comment_id>', methods=['PUT'])
@login_required
def edit_comment_info(comment_id):
    form = UpdateComment().validate_for_api()
    comment = Comment.objects(id=ObjectId(comment_id)).first()
    info = comment.update(text=form.text.data, status=form.status.data)
    return success_ret(data=info, msg='Update Success!')
