# -*- coding:utf-8 -*-
"""
图书模型
"""
import datetime
from bson import ObjectId
from mongoengine import *
from apps import db
from apps.core.error import ParameterException, NotFound


class Book(db.Document):
    title = StringField(required=True)
    author = StringField(required=True)
    summary = StringField(required=True)
    image = StringField(required=True)
    pub_time = DateTimeField()
    update_time = DateTimeField()

    meta = {
        'allow_inheritance': True,
        'indexes': ['title'],
        'ordering': ['-pub_time']
    }

    def __str__(self):  # 建议: 给每个模型增加 __str__ 方法，它返回一个具有可读性的字符串表示模型，可在调试和测试时使用
        return self.title + ' ' + self.author

    def save(self, *args, **kwargs):
        """
        这里用了一个重写save()函数的小技巧，因为每次更新博文时，文章对象的更新时间字段都会修改，而发布时间，只会在第一次发布时更新，
        这个小功能细节虽然也可以放到业务逻辑中实现，但那会使得业务逻辑变得冗长，在save()中实现更加优雅。
        """
        now = datetime.datetime.now()
        if not self.pub_time:
            self.pub_time = now
        self.update_time = now
        return super(Book, self).save(*args, **kwargs)

    def to_dict(self):
        book_dict = {}
        book_dict['id'] = str(self.id)
        book_dict['title'] = self.title
        book_dict['author'] = self.author
        book_dict['summary'] = self.summary
        book_dict['image'] = self.image
        return book_dict

    @classmethod
    def create_book(cls, form):
        book = Book.objects(title=form.title.data).first()
        if book is not None:
            raise ParameterException(msg='图书已存在')
        book = Book(title=form.title.data, author=form.author.data, summary=form.summary.data,
                    image=form.image.data)
        book.save()
        return True

    @classmethod
    def get_detail(cls, bid):
        book = Book.objects(id=ObjectId(bid)).first()
        if book is None:
            raise NotFound(msg='没有找到相关书籍')
        return book.to_dict()

    @classmethod
    def get_books(cls):
        books = Book.objects.all()  # .exclude('author')  排除某些字段
        if not books:
            raise NotFound(msg='没有找到相关书籍')
        data = [book.to_dict() for book in books]
        return data

    @classmethod
    def edit_book(cls, bid, form):
        book = Book.objects(id=ObjectId(bid)).first()
        if book is None:
            raise NotFound(msg='没有找到相关书籍')
        book.update(title=form.title.data, author=form.author.data, summary=form.summary.data,
                    image=form.image.data)
        return True

    @classmethod
    def remove_book(cls, bid):
        book = Book.objects(id=ObjectId(bid)).first()
        if book is None:
            raise NotFound(msg='没有找到相关书籍')
        book.delete()
        return True
