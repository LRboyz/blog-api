import datetime
from bson import ObjectId
from flask_jwt_extended import get_current_user
from mongoengine import *
from apps.models.user import User
from apps.utils.api_format import api_fields, api_exclude

# COMMENT_STATUS = ('public', 'invalid')  # 公开 | 无效


class Comment(DynamicDocument):
    comment_id = SequenceField()
    canDelete = BooleanField(default=True)
    canEdit = BooleanField(default=True)
    isLiked = BooleanField(default=False)
    reply_from = DictField()  # 评论人
    reply_to = DictField()    # 回复哪一位
    parent = StringField()  # 父级评论
    otherComments = ListField()
    create_time = DateTimeField()
    update_time = DateTimeField()
    status = BooleanField(default=True)
    post_id = StringField()  # 文章id
    text = StringField()
    votes = IntField(default=0)

    meta = {
        'allow_inheritance': True,
        'indexes': ['text'],
        'ordering': ['-create_time']
    }

    def to_dict(self):
        return api_exclude(self, '_cls', '_id')

    def save(self, *args, **kwargs):
        now = datetime.datetime.now()
        if not self.create_time:
            self.create_time = now
        self.update_time = now
        return super(Comment, self).save(*args, **kwargs)

    @classmethod
    def create_comment(cls, form):
        # 添加一级评论
        user = get_current_user()
        user = User.objects(id=ObjectId(user.id)).first()
        user_info = api_fields(user, 'avatar', '_id', 'nickname', 'username')
        comment = cls(text=form.text.data, reply_from=user_info)
        comment.save()
        return comment

    @classmethod
    def create_reply_comment(cls, form, parent_id):
        user = get_current_user()
        user = User.objects(id=ObjectId(user.id)).first()
        user_info = api_fields(user, 'avatar', '_id', 'nickname', 'username')
        reply_user = User.objects(id=ObjectId(form.reply_user_id.data)).first()  # 回复人数据
        reply_user_info = api_fields(reply_user, 'avatar', '_id', 'nickname', 'username')  # 回复人的信息
        reply_comment = cls(reply_from=user_info, reply_to=reply_user_info, text=form.text.data,
                            parent=parent_id)
        reply_comment.save()
        return api_exclude(reply_comment)




