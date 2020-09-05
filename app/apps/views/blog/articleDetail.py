from bson import ObjectId
from flask import Blueprint, jsonify
# import time
from apps.models.post import Post
from apps.utils.api_format import api_exclude

article_api = Blueprint('article', __name__)


# 文章详情
@article_api.route('/detail/<article_id>', methods=['GET'])
def article_detail(article_id):
    res = Post.objects(id=ObjectId(article_id)).first()
    res.update(inc__views=1)  # 浏览量+1
    detail = api_exclude(res)
    detail['author_info'] = api_exclude(res.author)
    return jsonify(code=200, msg="获取文章详情成功", data=detail)


# 文章归档
@article_api.route('/archive', methods=['GET'])
def article_archive():
    archive, cat_number = Post.get_detail_archive()
    return jsonify(mag="获取归类成功", code=200, archive=archive, cat_number=cat_number)
    # pass
