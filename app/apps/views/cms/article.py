from flask import Blueprint, jsonify, request
from apps.core.error import Success, RepeatException
from apps.core.token_auth import login_required
from apps.models.article import Article
from apps.utils.api_format import success_ret
from apps.validaters.forms import CreateArticleForm

article_api = Blueprint('article', __name__)


@article_api.route('/add/', methods=['POST'])
@login_required
def create_article():
    form = CreateArticleForm().validate_for_api()
    Article.create_article(form)
    return Success(msg="添加文章成功")


@article_api.route('/list/', methods=['GET'])
# @login_required
def get_all_article():
    keyword = request.args.get('searchKeyword')
    article, total = Article.get_articles(keyword)
    return success_ret(data=article, total=total)


@article_api.route('/edit/<aid>/', methods=['PUT'])
@login_required
def update_article(aid):
    form = CreateArticleForm().validate_for_api()
    Article.edit_article(aid, form)
    return Success(msg='更新文章信息成功')


@article_api.route('/<aid>/', methods=['GET'])
@login_required
def get_article(aid):
    # keyword = request.args.get('searchKeyword')
    article, total = Article.get_article(aid)
    return jsonify(article=article, error_code=0, total=total)


@article_api.route('/<aid>/', methods=['DELETE'])
@login_required
def delete_article(aid):
    Article.remove_article(aid)
    return Success(msg='删除文章成功')



