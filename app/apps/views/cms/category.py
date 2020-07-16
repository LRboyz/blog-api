from flask import Blueprint, jsonify, request
from apps.core.error import Success, RepeatException
from apps.core.token_auth import login_required
from apps.models.category import Category
from apps.utils import paginate
from apps.validaters.forms import CreateCategoryForm

cat_api = Blueprint('category', __name__)


@cat_api.route('/list/', methods=['GET'])
@login_required
def get_all_cat():
    cat_name = request.args.get('category_name')
    # print(cat_name)
    cat, total = Category.get_cats(cat_name)
    return jsonify(categorys=cat, error_code=0, total=total)


@cat_api.route('/<cid>/', methods=['GET'])
@login_required
def get_cat(cid):
    tag = Category.get_detail(cid)
    return jsonify(tag)


@cat_api.route('/edit/<cid>/', methods=['PUT'])
@login_required
def update_cat(cid):
    form = CreateCategoryForm().validate_for_api()
    Category.edit_cat(cid, form)
    return Success(msg='更新分类信息成功')


@cat_api.route('/add/', methods=['POST'])
@login_required
def create_cat():
    form = CreateCategoryForm().validate_for_api()
    exists = Category.objects(tag_name=form.category_name.data).first()
    if exists:
        raise RepeatException(msg="该分类已存在")
    Category.create_cat(form)
    return Success(msg="添加分类成功")


@cat_api.route('/<cid>/', methods=['DELETE'])
@login_required
def delete_cat(cid):
    Category.remove_cat(cid)
    return Success(msg='删除分类成功')


@cat_api.route('/correct/<cid>/', methods=['GET'])
def get_correct(cid):
    pass
