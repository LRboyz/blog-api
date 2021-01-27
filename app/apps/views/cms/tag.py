from flask import Blueprint, jsonify
from apps.core.error import Success
from apps.core.token_auth import login_required
from apps.models.article import Article
from apps.models.tag import Tag
from apps.utils import paginate
from apps.utils.api_format import success_ret
from apps.validaters.forms import CreateTagForm

tag_api = Blueprint('tag', __name__)


@tag_api.route('/list/', methods=['GET'])
# @login_required
def get_all_tag():
    items, total = Tag.get_tags()
    return success_ret(data=items, total=total)


@tag_api.route('/<tid>/', methods=['GET'])
# @login_required
def get_tag(tid):

    tag = Tag.get_detail(tid)
    return jsonify(tag)


@tag_api.route('/edit/<tid>/', methods=['PUT'])
@login_required
def update_tag(tid):
    form = CreateTagForm().validate_for_api()
    Tag.edit_tag(tid, form)
    return Success(msg='更新标签信息成功')


@tag_api.route('/add/', methods=['POST'])
@login_required
def create_tag():
    form = CreateTagForm().validate_for_api()
    Tag.create_tag(form)
    return Success(msg="添加标签成功")


@tag_api.route('/<tid>/', methods=['DELETE'])
@login_required
def delete_tag(tid):
    Tag.remove_tag(tid)
    return Success(msg='删除标签成功')


@tag_api.route('/correct/<tid>/', methods=['GET'])
def get_correct(tid):
    pass
