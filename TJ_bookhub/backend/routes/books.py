from flask import Blueprint, jsonify, request
from models import db, Book
from routes.auth import admin_required

books_bp = Blueprint('books', __name__,url_prefix='/api/books')

@books_bp.route('', methods=['GET'])
def get_books():
    # 检索图书（所有用户）
    query = Book.query
    title = request.args.get('title')
    author = request.args.get('author')
    category = request.args.get('category')
    
    if title:
        query = query.filter(Book.title.ilike(f'%{title}%'))
    if author:
        query = query.filter(Book.author.ilike(f'%{author}%'))
    if category:
        query = query.filter(Book.category == category)
    
    books = query.all()
    return jsonify([book.to_dict() for book in books])

@books_bp.route('', methods=['POST'])
@admin_required
def add_book():
    # 添加图书（管理员）
    data = request.get_json()
    book = Book(
        title=data['title'],
        author=data['author'],
        isbn=data['isbn'],
        publisher=data.get('publisher'),
        publish_date=data.get('publish_date'),
        total_copies=data.get('total_copies', 1),
        available_copies=data.get('available_copies', 1),
        category=data.get('category'),
        description=data.get('description')
    )
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_dict()), 201

@books_bp.route('/<int:id>', methods=['PUT'])
@admin_required
def update_book(id):
    # 更新图书（管理员）
    book = Book.query.get_or_404(id)
    data = request.get_json()
    
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    # 更新其他字段...
    
    db.session.commit()
    return jsonify(book.to_dict())

@books_bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_book(id):
    # 删除图书（管理员）
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'}), 200

@books_bp.route('/<int:id>', methods=['GET'])
def get_single_book(id):
    # 获取图书详情（所有用户）
    book = Book.query.get_or_404(id)
    return jsonify(book.to_dict())