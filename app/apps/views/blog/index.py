import random

from flask import Blueprint, jsonify, request
# import time
from apps.models.category import Category
from apps.models.post import Post
from apps.models.tag import Tag
from apps.models.user import User
from apps.utils import paginate
from apps.utils.api_format import success_ret

blog_api = Blueprint('blog', __name__)


# 首页文章列表
@blog_api.route('/article/list', methods=['GET'])
def article_list():
    start, count = paginate()  # 获取分页配置
    tag_name = request.args.get('tag_name')
    category_name = request.args.get('category_name')
    if category_name:
        posts = Post.objects(is_audit=True).filter(category__contains=category_name).skip(start).limit(count).all()
    elif tag_name:
        posts = Post.tags.objects(is_audit=True).filter(tag_name__contains=tag_name).skip(start).limit(count).all()
    else:
        posts = Post.objects(is_audit=True).skip(start).limit(count).all()  # .exclude('author')  排除某些字段
    post = [p.to_dict() for p in posts]
    current_total = posts.count()
    total = Post.objects.all().count()
    # time.sleep(3)
    return success_ret(data=post, msg='获取文章成功！', total=total, current_total=current_total)


# 首页分类列表
@blog_api.route('/category/list', methods=['GET'])
def category_list():
    start, count = paginate()
    cats = Category.objects.skip(start).limit(count).all()
    cat = [c.to_dict() for c in cats]
    total = Category.objects.all().count()
    return success_ret(data=cat, total=total, msg="获取分类列表成功")


# 首页热门文章列表
@blog_api.route('/hot/list', methods=['GET'])
def hot_article_list():
    posts = Post.objects.order_by('-pub_time').limit(10)
    hot_list = [h.to_dict() for h in posts]
    return success_ret(msg="获取热门文章列表成功", data=hot_list)


# 首页Tag标签列表
@blog_api.route('tag/list', methods=['GET'])
def blog_tag_list():
    items, total = Tag.get_tags()
    return success_ret(data=items, total=total)


# 首页用户信息
@blog_api.route('user')
def index_user_list():
    # start, count = paginate()
    users = User.objects.limit(10).all()
    user_list = [item.to_dict() for item in users]
    return success_ret(data=user_list, msg="获取用户信息成功")
    # pass

# 生成测试数据
# @blog_api.route('/article/test')
# def test_data():
#     number = random.sample(range(0, 10), 10)
#     test_title = "测试标题{0}".format(number)
#     for i in range(200):
#         post = Post(title=test_title, content='测试数据！！！！！！！')
#         post.save()
#     return jsonify(msg="添加数据成功！", code=200)


