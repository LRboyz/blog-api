from collections import namedtuple

from flask import request, current_app
from apps.core.error import ParameterException


def get_page_from_query():
    page_default = current_app.config.get('PAGE_DEFAULT')
    page = int(request.args.get('page', page_default if page_default else 0))
    return page


def paginate():
    count = int(request.args.get('count', current_app.config.get('COUNT_DEFAULT') if current_app.config.get(
        'COUNT_DEFAULT') else 5))
    start = int(request.args.get('page', current_app.config.get('PAGE_DEFAULT') if current_app.config.get(
        'PAGE_DEFAULT') else 0))
    count = 15 if count >= 15 else count
    start = start * count
    if start < 0 or count < 0:
        raise ParameterException()
    return start, count


