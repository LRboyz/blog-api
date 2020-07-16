from flask import Blueprint, jsonify

from apps.core.error import Success
from apps.models.book import Book
from apps.validaters.forms import CreateOrUpdateBookForm

book_api = Blueprint('book', __name__)


@book_api.route('/<bid>/', methods=['GET'])
# @login_required
def get_book(bid):
    book = Book.get_detail(bid)
    return jsonify(book)


@book_api.route('/list', methods=['GET'])
# @login_required
def get_books():
    books = Book.get_books()
    return jsonify(error_code=0, books=books)


@book_api.route('/add/', methods=['POST'])
def add_book():
    form = CreateOrUpdateBookForm().validate_for_api()
    Book.create_book(form)
    return jsonify(error_code=201, msg='添加图书成功')


@book_api.route('/edit/<bid>/', methods=['PUT'])
def update_book(bid):
    form = CreateOrUpdateBookForm().validate_for_api()
    Book.edit_book(bid, form)
    return Success(msg='更新图书成功')


@book_api.route('/<bid>/', methods=['DELETE'])
def delete_book(bid):
    Book.remove_book(bid)
    return Success(msg='删除图书成功')


