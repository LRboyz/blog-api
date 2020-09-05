from bson import ObjectId
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_current_user

from apps.core.error import NotFound, ParameterException, Success
from apps.core.token_auth import admin_required
from apps.models.permissions import append_permission
from apps.models.user import User
from apps.utils import paginate
from apps.utils.logger import Logger
from apps.validaters.forms import AdminUpdateInfoForm, ResetPasswordForm

admin_api = Blueprint('admin', __name__)


@admin_api.route('/users', methods=['GET'])
# @admin_required
def user_list():
    start, count = paginate()
    role = request.args.get('role')
    if role:
        users = User.objects(role=role).skip(start).limit(count).all()
    else:
        users = User.objects.skip(start).limit(count).all()  # .exclude('author')  排除某些字段
    if not users:
        raise NotFound(msg='暂无此用户')
    items = [user.to_dict() for user in users]
    total = users.count()
    return jsonify(items=items, total=total, code=200)


@admin_api.route('/<uid>', methods=['PUT'])
@Logger(template='{user.username}修改了信息')
@admin_required
def edit_info(uid):
    form = AdminUpdateInfoForm().validate_for_api()
    user = User.objects(id=uid).first()
    user.update(set__email=form.email.data, set__role=form.role.data)
    return Success(msg='信息修改成功！')


@admin_api.route('/password/<uid>', methods=['PUT'])
@Logger(template='{user.username}修改了密码')
@admin_required
def update_password(uid):
    form = ResetPasswordForm().validate_for_api()
    user = User.objects(id=uid).first()
    user.update(set___password=form.new_password.data)
    return Success(msg='密码修改成功！')


@admin_api.route('/<uid>', methods=['DELETE'])
@Logger(template='{user.username}删除了一个用户')
@admin_required
def delete_info(uid):
    info = User.objects(id=ObjectId(uid)).first()
    # print(info)
    if info is None:
        raise NotFound(msg='无此用户！')
    info.delete()
    return Success(msg="删除用户成功！")
