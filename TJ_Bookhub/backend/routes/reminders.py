from flask import Blueprint, jsonify, request
from models import db, Reminder
from utils.jwt import jwt_required

reminders_bp = Blueprint('reminders', __name__, url_prefix='/api/reminders')

@reminders_bp.route('', methods=['GET'])
@jwt_required
def get_reminders():
    try:
        user_id = request.user.get('user_id')
        if not user_id:
            return jsonify({'code': 404, 'msg': '错误！请重新登录'}), 404
        
        reminders = Reminder.query.filter_by(user_id=user_id).order_by(Reminder.created_time.desc()).all()
        data = [
            {
                'id': r.id,
                'is_read': r.is_read,
                'content': r.content,
                'created_time': r.created_time.strftime('%Y-%m-%d')
            }
            for r in reminders
        ]
        return jsonify({'code': 200, 'msg': '获取预期提醒成功', 'data': data})
    
    except Exception as e:
        return jsonify({'code': 500, 'msg': '数据库内部错误,请稍后重试'}), 500
    

@reminders_bp.route('/<int:reminder_id>', methods=['PUT'])
@jwt_required
def mark_reminder_as_read(reminder_id):
    try:
        reminder = Reminder.query.filter_by(id=reminder_id).first()
        if not reminder:
            return jsonify({'code': 404, 'msg': '提醒不存在'}), 404
        
        reminder.is_read = True
        db.session.commit()
        return jsonify({'code': 200, 'msg': '标记为已读成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'msg': '数据库内部错误,请稍后重试'}), 500