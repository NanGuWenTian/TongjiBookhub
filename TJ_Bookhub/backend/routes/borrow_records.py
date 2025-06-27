from flask import Blueprint, jsonify, request
from models import db, BorrowRecord, Reminder
from utils.jwt import jwt_required
from datetime import datetime, date

borrow_records_bp = Blueprint('borrow_records', __name__, url_prefix='/api/borrow_records')

@borrow_records_bp.route('', methods=['GET'])
@jwt_required
def get_borrow_records():
    try:
        user_id = request.user.get('user_id')
        if not user_id:
            return jsonify({'code': 404, 'msg': '错误！请重新登录'}), 404
        
        records = BorrowRecord.query.filter_by(user_id=user_id).order_by(BorrowRecord.borrow_date.desc()).all()

        data = []
        for record in records:
            data.append({
                'id': record.id,
                'bookId': record.book_id,
                'borrowDate': record.borrow_date.isoformat() if record.borrow_date else None,
                'dueDate': record.due_date.isoformat() if record.due_date else None,
                'returnDate': record.return_date.isoformat() if record.return_date else None,
                'status': record.status,
                'title': record.book.title,
                'author': record.book.author,
                'cover': record.book.cover_image
            })

        return jsonify({'code': 200, 'msg': '获取借阅记录成功', 'data': data})
    except Exception as e:
        return jsonify({'code': 500, 'msg': '数据库内部错误,请稍后重试'}), 500
    

@borrow_records_bp.route('/overdue_status', methods=['GET'])
@jwt_required
def check_overdue_status():
    try:
        user_id = request.user.get('user_id')

        now = datetime.now()
        overdue_records = BorrowRecord.query.filter_by(user_id=user_id, status='borrowed').filter(BorrowRecord.due_date < now).all()
        
        reminder_created = False

        for record in overdue_records:
            record.status = 'overdued'
            existing_reminder = Reminder.query.filter_by(
                user_id=user_id,
                book_id=record.book_id,
                created_time=date.today()
            ).first()

            if not existing_reminder:
                reminder = Reminder(
                    user_id=user_id,
                    created_time=date.today(),
                    content=f"您借阅的《{record.book.title}》已逾期，请尽快归还。",
                    is_read=False,
                    book_id=record.book_id
                )
                db.session.add(reminder)
                reminder_created = True


        if overdue_records or reminder_created:
            db.session.commit()

        return jsonify({
            'code': 200,
            'hasOverdue': len(overdue_records) > 0,
            'msg': '有逾期记录' if overdue_records else '无逾期记录'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'msg': '数据库内部错误,请稍后重试'}), 500
