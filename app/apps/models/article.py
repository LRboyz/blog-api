# -*- coding:utf-8 -*-
"""
博客文章模型
"""
import datetime

import mongoengine
from bson import ObjectId
from mongoengine import *
from apps import db
from apps.core.error import ParameterException, NotFound
from apps.models.category import Category
from apps.models.comment import Comment

from apps.models.tag import Tag
from apps.models.user import User
from apps.utils import paginate
from apps.utils.api_format import error_ret, api_exclude


class Article(Document):
    title = StringField(max_length=255, required=True)
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
    author = ReferenceField(User, reverse_delete_rule=CASCADE)  # 级联删除， 如果author被删除，则他发布的所有东西都被删除
    category = ReferenceField(Category, reverse_delete_rule=NULLIFY)
    is_audit = BooleanField()  # 发布或拉黑
    tags = ListField(ReferenceField(Tag, reverse_delete_rule=PULL))
    user_info = ReferenceField(User)
    article_type = IntField(choices=((0, '原创'), (1, '转载'), (2, '翻译')), default=0)  # 文章类型

    meta = {
        'allow_inheritance': True,  # 允许被继承
        'indexes': ['title', 'author'],  # 索引字段，后续按这两个字段值查询时可以加快速度
        'ordering': ['-pub_time']  # 表示按 pub_time 降序排列，没有减号表示升序排列
    }

    def save(self, *args, **kwargs):
        """
        这里用了一个重写save()函数的小技巧，因为每次更新博文时，文章对象的更新时间字段都会修改，而发布时间，只会在第一次发布时更新，
        这个小功能细节虽然也可以放到业务逻辑中实现，但那会使得业务逻辑变得冗长，在save()中实现更加优雅。
        """
        now = datetime.datetime.now()
        if not self.pub_time:
            self.pub_time = now
        self.update_time = now
        return super(Article, self).save(*args, **kwargs)

    # def to_dict(self):
    #     article_dict = self.to_mongo().to_dict()
    #     article_dict['id'] = article_dict['_id']
    #     article_dict['author'] = [user.to_dict() for user in User.objects(id=ObjectId(self.author_id))]
    #     del article_dict['_id']
    #     return article_dict

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
        article = cls.objects(title=form.title.data).first()
        if article is not None:
            raise ParameterException(msg='文章已存在')
        # tags = cls.update_tag_field(form.tags.data)
        # tags = [Tag(tag_name=item).save() for item in form.tags.data]
        # category = [Category(category_name=item).save() for item in form.category.data]
        article = Article(title=form.title.data, banner=form.banner.data,
                          content=form.content.data,
                          recommend=form.recommend.data, keyword=form.keyword.data, source=form.source.data,
                          is_audit=form.is_audit.data, article_type=form.article_type.data,
                          introduction=form.introduction.data)
        article.category = ObjectId(form.category.data)
        article.tags = [ObjectId(tag_id) for tag_id in form.tags.data]
        article.save()
        return True
        # user = get_current_user()
        # user_info = User.objects(id=user.id).first()
        # user_info.save()

        # if form.tags.data:  # 这个逻辑是找出来这个标签所对应的文章，用聚合查询
        #     tag_group = cls._get_collection().aggregate([
        #         {'$unwind': '$tags'},  # 将tags里的数据一个个分解数组
        #         {'$group': {'_id': '$tags', 'article_count': {'$sum': 1}}},  # 分组：按tag名称分组
        #         {'$project': {'_id': 0, 'tags': '$_id', 'article_count': 1}},  # 去掉不感兴趣的 _id 字段
        #         {'$sort': {'article_count': -1}}])  # sort 对 num_of_tag 字段排序
        #     for t in tag_group:
        #         if Tag.objects(tag_name=t['tags']).first():
        #             tags = Tag.objects(tag_name=t['tags']).first()
        #             tags.update(remove=True, tag_name=t['tags'], article_count=t['article_count'])
        #         else:
        #             tags = Tag(tag_name=t['tags'], article_count=t['article_count'])
        #             tags.save()

    @classmethod
    def get_detail_archive(cls):
        cursor = Article.objects.aggregate([{'$sample': {'size': 5}}])  # 随机返回五篇文章
        random_articles = []
        for item in cursor:
            item['_id'] = str(item['_id'])
            random_articles.append(item)
        cat_number = Article.objects.all().item_frequencies("category")  # 统计分类下的文章数量
        return random_articles, cat_number

    @classmethod
    def get_articles(cls, article_name):
        # 获取分页配置
        start, count = paginate()
        if article_name:
            articles = Article.objects.filter(title__icontains=article_name)  # 查询字段包含cat_name的对象
        else:
            articles = Article.objects.skip(start).limit(count).all()  # .exclude('author')  排除某些字段
        article_list = []
        for item in articles:
            category = api_exclude(item.category, '_cls')
            tags = [api_exclude(tag, '_cls') for tag in item.tags]
            article_list.append(api_exclude(item, '_cls'))
            for article in article_list:
                article['category'] = category
                article['tags'] = tags
        total = articles.count()
        return article_list, total

    @classmethod
    def get_article(cls, aid):
        if not aid:
            raise NotFound(msg='没有找到此文章')
        article = Article.objects(id=ObjectId(aid)).first()
        total = len(article)
        return api_exclude(article), total

    @classmethod
    def edit_article(cls, aid, form):
        article = Article.objects(id=ObjectId(aid)).first()
        if article is None:
            raise NotFound(msg='没有找到相关文章')
        article.update(title=form.title.data, banner=form.banner.data,content=form.content.data,
                       category=form.category.data, tags=form.tags.data, recommend=form.recommend.data,
                       keyword=form.keyword.data, source=form.source.data, is_audit=form.is_audit.data,
                       article_type=form.article_type.data, introduction=form.introduction.data)
        return True

    @classmethod
    def remove_article(cls, aid):
        article = Article.objects(id=aid).first()
        if article is None:
            raise NotFound(msg='没有找到相关文章')
        article.delete()
        return True

    # @classmethod
    # def update_category_field(cls, form):
    #     category_list = []
    #     for item in form:
    #         category = Category.objects(category_name=item).first()
    #         if category is None:
    #             Category(category_name=item).save()
    #         else:
    #             category.update(count=category.count+1)
    #         category_list.append(api_exclude(Category(category_name=item)))
    #     return category_list
    #
    # @classmethod
    # def update_tag_field(cls, form):
    #     print(form, '99999')
    #     tag_list = []
    #     for item in form:
    #         tag = Tag.objects(tag_name=item).first()
    #         if tag is None:
    #             Tag(tag_name=item).save()
    #         else:
    #             tag.update(count=tag.count + 1)
    #         tag_list.append(api_exclude(Tag(tag_name=item)))
    #     return tag_list

    @classmethod
    def computed_tag_list(cls):
        tags_group = cls._get_collection().aggregate([{'$unwind':'$category'},{'$group':{'_id':'$category', 'num':{'$sum':1}}}])
        return [dict(item) for item in tags_group]
