from flask import Blueprint, jsonify, request
from apps.core.error import Success, RepeatException
from apps.core.token_auth import login_required
from apps.models.post import Post
from apps.validaters.forms import CreatePostForm

post_api = Blueprint('post', __name__)


@post_api.route('/add/', methods=['POST'])
@login_required
def create_article():
    form = CreatePostForm().validate_for_api()
    Post.create_article(form)
    return Success(msg="添加文章成功")


@post_api.route('/list/', methods=['GET'])
@login_required
def get_all_post():
    keyword = request.args.get('searchKeyword')
    article, total = Post.get_posts(keyword)
    return jsonify(articles=article, error_code=0, total=total)


@post_api.route('/edit/<aid>/', methods=['PUT'])
@login_required
def update_cat(aid):
    form = CreatePostForm().validate_for_api()
    Post.edit_post(aid, form)
    return Success(msg='更新文章信息成功')


@post_api.route('/<aid>/', methods=['GET'])
@login_required
def get_post(aid):
    # keyword = request.args.get('searchKeyword')
    article, total = Post.get_post(aid)
    return jsonify(article=article, error_code=0, total=total)


@post_api.route('/<aid>/', methods=['DELETE'])
@login_required
def delete_article(aid):
    Post.remove_post(aid)
    return Success(msg='删除文章成功')



