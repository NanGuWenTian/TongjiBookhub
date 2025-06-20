from flask import Blueprint, jsonify, request
from models import db, BorrowRecord, Book, User
from datetime import datetime, timedelta
from routes.auth import login_required, admin_required

borrows_bp = Blueprint('borrows', __name__)

@borrows_bp.route('/borrows', methods=['POST'])
@login_required
def borrow_book():
    # 借阅图书（用户）
    user_id = request.user_id  # 从认证中获取
    data = request.get_json()
    book_id = data['book_id']
    
    book = Book.query.get_or_404(book_id)
    if book.available_copies <= 0:
        return jsonify({'error': 'No available copies'}), 400
    
    # 减少可用副本
    book.available_copies -= 1
    
    # 创建借阅记录
    borrow = BorrowRecord(
        user_id=user_id,
        book_id=book_id,
        borrow_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=30),
        status='borrowed'
    )
    db.session.add(borrow)
    db.session.commit()
    
    return jsonify(borrow.to_dict()), 201

@borrows_bp.route('/borrows/<int:id>/return', methods=['POST'])
@login_required
def return_book(id):
    # 归还图书（用户）
    borrow = BorrowRecord.query.get_or_404(id)
    
    # 验证当前用户是否有权限归还
    if borrow.user_id != request.user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    borrow.return_date = datetime.utcnow()
    borrow.status = 'returned'
    
    # 增加可用副本
    book = Book.query.get(borrow.book_id)
    book.available_copies += 1
    
    db.session.commit()
    return jsonify(borrow.to_dict())

@borrows_bp.route('/borrows', methods=['GET'])
@login_required
def get_user_borrows():
    # 获取用户借阅记录（用户和管理员）
    user_id = request.args.get('user_id', request.user_id)
    
    # 管理员可以查看所有用户的借阅记录
    if not request.is_admin and user_id != request.user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    borrows = BorrowRecord.query.filter_by(user_id=user_id).all()
    return jsonify([borrow.to_dict() for borrow in borrows])

@borrows_bp.route('/overdue', methods=['GET'])
def get_overdue_borrows():
    # 获取逾期未还的借阅记录（管理员）
    overdue_borrows = BorrowRecord.query.filter(
        BorrowRecord.due_date < datetime.utcnow(),
        BorrowRecord.status == 'borrowed'
    ).all()
    
    return jsonify([borrow.to_dict() for borrow in overdue_borrows])