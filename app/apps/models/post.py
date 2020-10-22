# -*- coding:utf-8 -*-
"""
博客文章模型
"""
import datetime

from bson import ObjectId
from flask_jwt_extended import get_current_user
from mongoengine import *
from apps import db
from apps.core.error import ParameterException, NotFound
from apps.models.comment import Comment

from apps.models.tag import Tag
from apps.models.user import User
from apps.utils import paginate
from apps.utils.api_format import error_ret


class Post(DynamicDocument):

    title = StringField(max_length=255, default='new blog', required=True)
    banner = StringField()  # 文章banner图
    pub_time = DateTimeField()  # 发布时间
    update_time = DateTimeField()  # 更新时间
    introduction = StringField()  # 文章摘要
    views = IntField(default=0)  # 文章浏览量
    likes = IntField(default=0)  # 点赞数量
    recommend = BooleanField()  # 是否推荐
    keyword = StringField()  # 关键词
    source = StringField()  # 文章来源
    comments = ListField(ReferenceField(Comment))
    commentsCount = IntField(default=0)  # 评论数量
    content = StringField(required=True)
    author = ReferenceField(User, reverse_delete_rule=db.CASCADE)  # 级联删除， 如果author被删除，则他发布的所有东西都被删除
    category = StringField()  # ReferenceField(Category, reverse_delete_rule=db.NULLIFY)
    is_audit = BooleanField()  # 发布或拉黑
    tags = ListField()  # ReferenceField(Tag, reverse_delete_rule=db.PULL)
    # tags）中只有 tag01 被删除，其它标签还在，合理！
    user_info = ReferenceField(User)
    # is_draft = db.BooleanField(default=False)  # 是否草稿
    post_type = IntField()  # 文章类型

    def save(self, *args, **kwargs):
        """
        这里用了一个重写save()函数的小技巧，因为每次更新博文时，文章对象的更新时间字段都会修改，而发布时间，只会在第一次发布时更新，
        这个小功能细节虽然也可以放到业务逻辑中实现，但那会使得业务逻辑变得冗长，在save()中实现更加优雅。
        """
        now = datetime.datetime.now()
        if not self.pub_time:
            self.pub_time = now
        self.update_time = now
        return super(Post, self).save(*args, **kwargs)

    def to_dict(self):
        post_dict = self.to_mongo().to_dict()
        post_dict['id'] = post_dict['_id']
        post_dict['author'] = [user.to_dict() for user in User.objects(id=ObjectId(self.author_id))]
        del post_dict['_id']
        return post_dict

    @classmethod
    def first_or_404(cls, pid):
        try:
            res = cls.objects.with_id(pid)
            if res is None:
                return error_ret(msg="没有找到该文章", code=404)
            else:
                return res
        except Exception as e:
            print(e)

        # pass

    @classmethod
    def create_article(cls, form):
        post = cls.objects(title=form.title.data).first()
        if post is not None:
            raise ParameterException(msg='文章已存在')
        user = get_current_user()
        user_info = User.objects(id=user.id).first()
        user_info.save()
        post = Post(title=form.title.data, banner=form.banner.data, author_id=form.author_id.data,
                    content=form.content.data, category=form.category.data, tags=form.tags.data, recommend=
                    form.recommend.data, keyword=form.keyword.data, source=form.source.data, is_audit=form.is_audit.data
                    , post_type=form.post_type.data, introduction=form.introduction.data, author=user_info)
        post.save()
        if form.tags.data:  # 这个逻辑是找出来这个标签所对应的文章，用聚合查询
            tag_group = cls._get_collection().aggregate([
                {'$unwind': '$tags'},  # 将tags里的数据一个个分解数组
                {'$group': {'_id': '$tags', 'article_count': {'$sum': 1}}},  # 分组：按tag名称分组
                {'$project': {'_id': 0, 'tags': '$_id', 'article_count': 1}},  # 去掉不感兴趣的 _id 字段
                {'$sort': {'article_count': -1}}])  # sort 对 num_of_tag 字段排序
            for t in tag_group:
                if Tag.objects(tag_name=t['tags']).first():
                    tags = Tag.objects(tag_name=t['tags']).first()
                    tags.update(remove=True, tag_name=t['tags'], article_count=t['article_count'])
                else:
                    tags = Tag(tag_name=t['tags'], article_count=t['article_count'])
                    tags.save()
        return True

    @classmethod
    def get_detail_archive(cls):
        cursor = Post.objects.aggregate([{'$sample': {'size': 5}}])  # 随机返回五篇文章
        random_articles = []
        for item in cursor:
            item['_id'] = str(item['_id'])
            random_articles.append(item)
        cat_number = Post.objects.all().item_frequencies("category")  # 统计分类下的文章数量
        return random_articles, cat_number

    @classmethod
    def get_posts(cls, post_name):
        start, count = paginate()  # 获取分页配置
        if post_name:
            posts = Post.objects.filter(title__icontains=post_name)  # 查询字段包含cat_name的对象
        else:
            posts = Post.objects.skip(start).limit(count).all()  # .exclude('author')  排除某些字段
        post = [p.to_dict() for p in posts]
        total = posts.count()
        return post, total

    @classmethod
    def get_post(cls, aid):
        if not aid:
            raise NotFound(msg='没有找到此文章')
        post = Post.objects(id=ObjectId(aid)).first()
        post = cls.to_dict(post)
        total = len(post)
        return post, total

    @classmethod
    def edit_post(cls, aid, form):
        post = Post.objects(id=ObjectId(aid)).first()
        if post is None:
            raise NotFound(msg='没有找到相关文章')
        post.update(title=form.title.data, banner=form.banner.data,
                    content=form.content.data, category=form.category.data, tags=form.tags.data, recommend=
                    form.recommend.data, keyword=form.keyword.data, source=form.source.data, is_audit=form.is_audit.data
                    , post_type=form.post_type.data, introduction=form.introduction.data)
        return True

    @classmethod
    def remove_post(cls, aid):
        post = Post.objects(id=ObjectId(aid)).first()
        if post is None:
            raise NotFound(msg='没有找到相关文章')
        post.delete()
        return True
