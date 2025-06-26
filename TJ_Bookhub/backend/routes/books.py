from flask import Blueprint, jsonify, request
from models import db, Book, BookCategory, BorrowRecord, CategoryBorrowData
from utils.jwt import jwt_required
from datetime import datetime, timedelta
# from routes.auth import admin_required

books_bp = Blueprint('books', __name__, url_prefix='/api/books')

@books_bp.route('', methods=['GET'])
@jwt_required
def get_books():
    # 检索图书（所有用户）
    query = Book.query
    title = request.args.get('title')
    author = request.args.get('author')
    category = request.args.get('category')

    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 5))
    except ValueError:
        return jsonify({'code': 400, 'msg': '分页参数错误'}), 400
    
    if title:
        query = query.filter(Book.title.ilike(f'%{title}%'))
    if author:
        query = query.filter(Book.author.ilike(f'%{author}%'))
    if category:
        matched_categories = BookCategory.query.filter(BookCategory.name.ilike(f'%{category}%')).all()
        if matched_categories:
            matched_ids = [cat.id for cat in matched_categories]
            query = query.filter(Book.category_id.in_(matched_ids))
        else:
            return jsonify({'code': 200, 'msg': '成功', 'data': [], 'total': 0}), 200
    
    pagination = query.order_by(Book.id.desc()).paginate(page=page, per_page=limit, error_out=False)
    books = pagination.items
    total = pagination.total

    data = []
    for book in books:
        book_dict = book.to_dict()
        category = BookCategory.query.get(book.category_id)
        book_dict['category'] = category.name if category else None
        data.append(book_dict)

    return jsonify({'code': 200, 'msg': '成功', 'data': data, 'total': total})


@books_bp.route('/<int:id>', methods=['GET'])
@jwt_required
def get_bookDetails(id):
    # 获取图书详情（所有用户）
    try:
        book = Book.query.get(id)
        if not book:
            return jsonify({'code': 404, 'msg': '图书不存在'}), 404

        category = BookCategory.query.get(book.category_id)
        book_dict = book.to_dict()
        book_dict['category'] = category.name if category else None
        return jsonify({'code': 200, 'msg': '成功', 'data': book_dict})
    except Exception as e:
        return jsonify({'code': 500, 'msg': '数据库内部错误,请稍后重试'}), 500



@books_bp.route('/<int:id>/status', methods=['GET'])
@jwt_required
def get_bookStatus(id):
    # 获取图书状态（所有用户）
    try:
        user_id = request.user.get('user_id')
        if not user_id:
            return jsonify({'code': 404, 'msg': '用户不存在'}), 404

        book = Book.query.get(id)
        if not book:
            return jsonify({'code': 404, 'msg': '图书不存在'}), 404
        
        borrowed = BorrowRecord.query.filter(
            BorrowRecord.user_id == user_id,
            BorrowRecord.book_id == id,
            BorrowRecord.status.in_(['borrowed', 'overdued'])
        ).first()
       
        is_borrowed = borrowed is not None

        return jsonify({'code': 200, 'msg': '成功', 'data': {'is_borrowed': is_borrowed, 'due_date': borrowed.due_date.isoformat()  if borrowed else None}})
    except Exception as e:
        return jsonify({'code': 500, 'msg': '数据库内部错误,请稍后重试'}), 500


@books_bp.route('/<int:id>/borrow/<int:during>', methods=['POST'])
@jwt_required
def borrow_book(id, during):
    # 借阅图书（所有用户）
    try:
        user_id = request.user.get('user_id')
        if not user_id:
            return jsonify({'code': 404, 'msg': '用户不存在'}), 404

        book = Book.query.get(id)
        if not book:
            return jsonify({'code': 404, 'msg': '图书不存在'}), 404
        
        if book.available_copies <= 0:
            return jsonify({'code': 400, 'msg': '图书已借完'}), 400
        
        book.available_copies -= 1
        book.borrow_counts += 1

        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=during)
        new_record = BorrowRecord(
            user_id=user_id,
            book_id=id,
            borrow_date=borrow_date,
            due_date=due_date,
            return_date=None,
            status='borrowed'
        )
        db.session.add(new_record)

        category_id = book.category_id
        year = borrow_date.year
        month = borrow_date.month

        existing_stat = CategoryBorrowData.query.filter_by(
            category_id=category_id,
            year=year,
            month=month
        ).first()

        if existing_stat:
            existing_stat.borrow_counts += 1
        else:
            new_stat = CategoryBorrowData(
                category_id=category_id,
                year=year,
                month=month,
                borrow_counts=1
            )
            db.session.add(new_stat)

        db.session.commit()
        return jsonify({'code': 200, 'msg': '借阅成功'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'msg': '数据库内部错误,请稍后重试'}), 500
    


@books_bp.route('/<int:id>/return', methods=['POST'])
@jwt_required
def return_book(id):
    # 归还图书（所有用户）
    try:
        user_id = request.user.get('user_id')
        if not user_id:
            return jsonify({'code': 404, 'msg': '用户不存在'}), 404

        book = Book.query.get(id)
        if not book:
            return jsonify({'code': 404, 'msg': '图书不存在'}), 404
        
        borrowed = BorrowRecord.query.filter(
            BorrowRecord.user_id == user_id,
            BorrowRecord.book_id == id,
            BorrowRecord.status.in_(['borrowed', 'overdued'])
        ).first()

        if not borrowed:
            return jsonify({'code': 400, 'msg': '图书未借出'}), 400
        
        borrowed.status = 'finished'
        borrowed.return_date = datetime.now()
        book.available_copies += 1
        db.session.commit()
        return jsonify({'code': 200, 'msg': '归还成功'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'msg': '数据库内部错误,请稍后重试'}), 500
    






@books_bp.route('/admin', methods=['GET'])
def get_books_admin():
    # 获取图书列表（管理员）
    query = Book.query
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 8, type=int)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    book_items = []
    for book in pagination.items:
        book_dict = book.to_dict()
        book_items.append(book_dict)

    return jsonify({
        'book_items': book_items,
        'total': pagination.total,
        'pages': pagination.pages,
        'page': page,
        'per_page': per_page
    })


@books_bp.route('/admin', methods=['POST'])
# @admin_required
def add_book_admin():
    # 添加图书（管理员）
    data = request.get_json()

    required_fields = ['title']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
        
    book = Book(
        title=data['title'],
        author=data['author'],
        isbn=data['isbn'],
        publisher=data.get('publisher'),
        publish_date=data.get('publish_date'),
        total_copies=data.get('total_copies', 1),
        available_copies=data.get('total_copies', 1),
        category_id=data.get('category_id'),
        description=data.get('description'),
        cover_image=data.get('cover_image'),
        rating=data.get('rating', 0.0),
        rating_counts=data.get('rating_counts', 0),
        borrow_counts=data.get('borrow_counts', 0)
    )
    db.session.add(book)
    try:
        db.session.commit()
        return jsonify({"message": "书籍添加成功", "id": book.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"书籍添加时出错: {str(e)}"}), 500


@books_bp.route('/admin/<int:id>', methods=['PUT'])
# @admin_required
def update_book(id):
    # 更新图书（管理员）
    book = Book.query.get_or_404(id)
    data = request.get_json()

    for field in ['title', 'author', 'isbn', 'publisher', 'category_id', 'description', 'cover_image']:
        if field in data:
            setattr(book, field, data[field])

    if 'publish_date' in data:
        try:
            book.publish_date = datetime.fromisoformat(data['publish_date']).date()
        except ValueError:
            return jsonify({"error": "Invalid publish_date format. Use ISO format like 2025-06-30T14:00:00"}), 400

    if 'total_copies' in data:
        counts = data['total_copies'] - book.total_copies + book.available_copies
        if counts < 0:
            return jsonify({"error": "暂时无法削减该图书数目，等所有图书回收后再削减"}), 400
        book.available_copies = counts
        book.total_copies = data['total_copies']

    try:
        db.session.commit()
        return jsonify({"message": "图书更新成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"更新图书时出错: {str(e)}"}), 500



@books_bp.route('/admin/<int:id>', methods=['DELETE'])
# @admin_required
def delete_book(id):
    # 删除图书（管理员）
    book = Book.query.get_or_404(id)

    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "活动删除成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"删除活动时出错: {str(e)}"}), 500

