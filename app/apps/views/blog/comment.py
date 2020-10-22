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
    return success_ret(msg='一级评论成功', data=api_exclude(comment, '_cls', '_id'))


@comment_api.route('<parent_id>', methods=['POST'])
@login_required
def reply_comment(parent_id):
    form = CreateCommentForm().validate_for_api()
    reply = Comment.create_reply_comment(form, parent_id)
    other_comments = [api_exclude(item, '_cls', '_id') for item in Comment.objects(parent=parent_id).all()]
    reply['other_comments'] = other_comments
    comment = Comment.objects(comment_id=parent_id).first()
    comment.update(otherComments=other_comments)
    return success_ret(msg='回复评论成功', data=reply)


@comment_api.route('/public', methods=['GET'])
def get_comment_list():
    post_id = request.args.get('post_id')
    post = Post.objects(id=ObjectId(post_id)).first()
    comment_list = [api_exclude(item, '_cls', '_id') for item in post.comments]
    total = len(comment_list)
    return success_ret(data=comment_list, total=total)


@comment_api.route('/user-like', methods=['POST'])
def like_comment():
    comment_id = request.json.get('comment_id')
    print(comment_id)
    comment = Comment.objects(comment_id=comment_id).all()
    comment.update(inc__votes=1)
    # Comment._get_collection().update({"repliedComments":}, {})
    return success_ret(msg='点赞成功！爱你么么哒')
    # pass
