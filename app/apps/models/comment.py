import datetime
import time

from bson import ObjectId
from mongoengine import *
# from apps.models.post import Post
from apps.models.user import User
from apps.utils.api_format import api_fields, api_exclude

COMMENT_STATUS = ('approved', 'pending', 'spam', 'deleted')


class Comment(DynamicDocument):
    canDelete = BooleanField(default=True)
    canEdit = BooleanField(default=True)
    isLiked = BooleanField(default=False)
    repliedComments = ListField()
    other_commends = DictField()
    create_time = DateTimeField()
    update_time = DateTimeField()
    status = StringField(choices=COMMENT_STATUS, default='pending')
    post_id = StringField()  # 文章id
    comment_user_id = StringField()  # 评论人id
    reply_id = StringField()  # 评论的id
    text = StringField()
    votes = IntField(default=0)

    meta = {
        'allow_inheritance': True,
        'indexes': ['text'],
        'ordering': ['-create_time']
    }

    def to_dict(self):
        comment_dict = self.to_mongo().to_dict()
        return comment_dict

    def save(self, *args, **kwargs):
        now = datetime.datetime.now()
        if not self.create_time:
            self.create_time = now
        self.update_time = now
        return super(Comment, self).save(*args, **kwargs)

    @classmethod
    def create_comment(cls, form):
        # 添加一级评论
        user = User.objects(id=ObjectId(form.comment_user_id.data)).first()
        user_info = api_fields(user, 'avatar', '_id', 'nickname', 'username')
        comment = cls(post_id=form.post_id.data, text=form.text.data, comment_user_id=form.comment_user_id.data,
                      user=user_info)
        comment.save()
        return comment

    @classmethod
    def create_reply_comment(cls, form, post_id):
        user = User.objects(id=ObjectId(form.comment_user_id.data)).first()  # 评论人数据
        user_info = api_fields(user, 'avatar', '_id', 'nickname', 'username')  # 评论人的信息
        reply_user = User.objects(id=ObjectId(form.reply_user_id.data)).first()  # 回复人数据
        reply_user_info = api_fields(reply_user, 'avatar', '_id', 'nickname', 'username')  # 回复人的信息
        reply_comment = cls(reply_user=reply_user_info, user=user_info, text=form.text.data)
        reply_comment.save()
        commend = cls.objects(comment_user_id=form.reply_user_id.data).first()  # 首先找出这条评论的信息来先
        commend.repliedComments.append(reply_comment)
        commend.save()
        rows = [api_exclude(item) for item in commend.repliedComments]
        commend.update(repliedComments=rows)
        print(commend.repliedComments)
        return reply_comment
        # return True

    @staticmethod
    def strtime_to_timestamp(val, formate="%Y-%m-%d %H:%M:%S", is_float=False):
        """
        将文本时间转换成时间戳
        :param val: 文本时间
        :param formate: 文本时间格式
        :param is_float: 是否需要浮点数时间戳，默认不需要，返回整数时间戳
        :return st: 返回时间戳
        """
        if isinstance(val, int):
            return val
        tmp = datetime.datetime.strptime(val, formate)
        st = time.mktime(tmp.timetuple())
        if is_float:
            return st
        return int(st)





