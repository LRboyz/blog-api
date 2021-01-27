from flask import Blueprint, jsonify
from apps.models.article import Article
from apps.utils.api_format import api_exclude, success_ret, error_ret

article_detail_api = Blueprint('article_detail', __name__)


# 文章详情
@article_detail_api.route('/detail/<article_id>', methods=['GET'])
def article_detail(article_id):
    try:
        res = Article.first_or_404(article_id)
        res.update(inc__views=1)  # 浏览量+1
        detail = api_exclude(res)
        detail['author_info'] = api_exclude(res.author)
        return success_ret(msg="获取文章详情成功", data=detail)
    except Exception as e:
        print(e)
        return error_ret(code=400, msg="查询文章详情页错误或不存在！")


# 文章点赞
@article_detail_api.route('/like/<article_id>', methods=['POST'])
def like_article(article_id):
    try:
        res = Article.first_or_404(article_id)
        res.update(inc__likes=1)  # 浏览量+1
        detail = api_exclude(res)
        detail['author_info'] = api_exclude(res.author)
        return success_ret(msg="点赞文章成功！")
    except Exception as e:
        print(e)
        return error_ret(code=400, msg="点赞失败！！")


# 文章归档
@article_detail_api.route('/archive', methods=['GET'])
def article_archive():
    try:
        archive, cat_number = Article.get_detail_archive()
        return jsonify(mag="获取归类成功", code=200, archive=archive, cat_number=cat_number)
    except Exception as e:
        print(e)
        return error_ret(code=400, msg="获取归类失败！")
