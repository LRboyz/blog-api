from bson import ObjectId
from flask import Blueprint, request
from apps.core.token_auth import login_required
from apps.models.comment import Comment
from apps.models.post import Post
from apps.utils.api_format import success_ret, api_exclude
from apps.validaters.forms import CreateCommentForm

comment_api = Blueprint('comment', __name__)


@comment_api.route('', methods=['POST'])
@login_required
def add_comment():
    form = CreateCommentForm().validate_for_api()
    comment = Comment.create_comment(form)
    post = Post.objects(id=ObjectId(form.post_id.data)).first()
    post.comments.append(comment)
    post.save()
    increment_count = post.commentsCount + 1
    post.update(commentsCount=increment_count)
    return success_ret(msg='一级评论成功', data=api_exclude(comment))


@comment_api.route('<post_id>', methods=['POST'])
def reply_comment(post_id):
    form = CreateCommentForm().validate_for_api()
    reply_comment = Comment.create_reply_comment(form, post_id)
    return success_ret(msg='回复评论成功', data=api_exclude(reply_comment))


@comment_api.route('/public', methods=['GET'])
def get_comment_list():
    post_id = request.args.get('post_id')
    print(post_id)
    comment_list = Comment.objects(post_id=post_id).all()
    print(comment_list)
    res = [item.to_dict() for item in comment_list]
    return success_ret(data=res)


@comment_api.route('/user-like', methods=['POST'])
def like_comment():
    comment_id = request.json.get('comment_id')
    print(comment_id)
    comment = Comment.objects(id=ObjectId(comment_id)).first()
    comment.update(inc__votes=1)
    print(comment)
    return success_ret(msg='点赞成功！爱你么么哒')
    # pass
