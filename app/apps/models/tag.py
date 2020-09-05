import datetime
import json

from bson import ObjectId
from flask import current_app
from mongoengine import *
from apps import db
from apps.core.error import NotFound, RepeatException
# from apps.models.post import Post
from apps.utils import paginate


class Tag(db.DynamicDocument):
    tag_name = StringField()
    article_count = IntField(default=0)  # 文章数量
    subscriber_count = IntField()  # 订阅数
    view_hits = IntField()  # 查看点击
    thumbnail = StringField()
    status = BooleanField()
    pub_time = DateTimeField()
    update_time = DateTimeField()

    meta = {
        'allow_inheritance': True,
        'indexes': ['tag_name'],
        'ordering': ['-pub_time']
    }

    def to_dict(self):
        tag_dict = self.to_mongo().to_dict()
        tag_dict['id'] = tag_dict['_id']
        del tag_dict['_id']
        return tag_dict

    # def to_dict(self):
    #     j = self.to_json()
    #     dicts = json.loads(j)
    #     dicts['id'] = dicts['_id']['$oid']  # 查出来的id字段： {'$oid': '5f0c5e6e82d8036913ac39d3'}，转成id
    #     dicts['pub_time'] = self.pub_time
    #     dicts['update_time'] = self.update_time
    #     del dicts['_id']  # 如果要删除id，执行这个方法
    #     return dicts

    def save(self, *args, **kwargs):
        now = datetime.datetime.now()
        if not self.pub_time:
            self.pub_time = now
        self.update_time = now
        return super(Tag, self).save(*args, **kwargs)

    @property
    def _thumbnail(self):
        site_domain = current_app.config.get('SITE_DOMAIN') if current_app.config.get(
            'SITE_DOMAIN') else "http://127.0.0.1:5000"
        if self.thumbnail is not None:
            return site_domain + self.thumbnail

    @classmethod
    def create_tag(cls, form):
        exists = Tag.objects(tag_name=form.tag_name.data).first()
        if exists:
            raise RepeatException(msg="该标签名已存在")
        tags = Tag(tag_name=form.tag_name.data, thumbnail=form.thumbnail.data, alias=form.alias.data,
                   status=form.status.data)
        tags.save()
        return True

    @classmethod
    def get_tags(cls):
        start, count = paginate()  # 获取分页配置
        tags = Tag.objects.skip(start).limit(count).all()  # .exclude('author')  排除某些字段
        items = [tag.to_dict() for tag in tags]
        total = tags.count()
        return items, total

    @classmethod
    def get_detail(cls, tid):
        tag = Tag.objects(id=ObjectId(tid)).first()
        if tag is None:
            raise NotFound(msg='没有找到相关标签')
        return tag.to_dict()

    @classmethod
    def remove_tag(cls, tid):
        tag = Tag.objects(id=ObjectId(tid)).first()
        if tag is None:
            raise NotFound(msg='没有找到相关标签')
        tag.delete()
        return True

    @classmethod
    def edit_tag(cls, tid, form):
        tag = Tag.objects(id=ObjectId(tid)).first()
        if tag is None:
            raise NotFound(msg='没有找到相关标签')
        tag.update(tag_name=form.tag_name.data, thumbnail=form.thumbnail.data, alias=form.alias.data,
                   status=form.status.data)
        return True

    @classmethod
    def get_correct(cls, tid):
        """
        所属文章数量
        :param tid:
        :return:
        """
        pass
