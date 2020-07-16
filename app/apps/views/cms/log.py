import math
import time

from flask import Blueprint, jsonify, request
from mongoengine import Q

from apps.core.error import ParameterException
from apps.core.token_auth import login_required
from apps.models.log import Log
from apps.utils import paginate, get_page_from_query
from apps.validaters.forms import LogFindForm

log_api = Blueprint('log', __name__)


@log_api.route('/logs')
@login_required
def get_logs():
    start, count = paginate()  # 获取分页配置
    result = Log.objects.skip(start).limit(count).all()
    items = [log.to_dict() for log in result]
    total = result.count()
    total_page = math.ceil(total/count)
    page = get_page_from_query()
    if not items:
        items = []
    return jsonify(page=page, count=count, total=total, items=items, total_page=total_page), 201


@log_api.route('/logs/user')
@login_required
def get_log_user():
    return jsonify(msg='暂时不返回此接口')


@log_api.route('/log/search')
@login_required
def search_log():
    form = LogFindForm().validate_for_api()
    keyword = request.args.get('keyword', default=None, type=str)
    if keyword is None or '':
        raise ParameterException(msg='搜索关键字不可为空')
    start, count = paginate()
    logs = Log.objects.filter(message__icontains=keyword)  # 查询字段message包含keyword的对象
    if form.start.data and form.end.data:
        # 将前端传来的时间转为时间戳
        start_time = int(time.mktime(time.strptime(form.start.data, "%Y-%m-%d %H:%M:%S"))*1000)
        end_time = int(time.mktime(time.strptime(form.end.data, "%Y-%m-%d %H:%M:%S"))*1000)
        # print(start_time, end_time)
        logs = logs.filter((Q(create_time__gte=start_time) & Q(create_time__lte=end_time)))
    total = logs.count()
    result = logs.skip(start).limit(count).all()
    items = [log.to_dict() for log in result]
    if not logs:
        items = []
    return jsonify(items=items, total=total, code=201)





