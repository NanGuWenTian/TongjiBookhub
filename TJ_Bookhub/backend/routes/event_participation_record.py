from flask import Blueprint, request, jsonify
from models import db, EventParticipationRecord, User, Event
from datetime import datetime
from collections import defaultdict
import json

event_participation_record_bp = Blueprint('event_participation_record', __name__, url_prefix='/api/event_participation_record')

# 创建活动参与记录-测试正确
@event_participation_record_bp.route('', methods=['POST'])
def create_record():
    # 修改1：从JSON请求体中获取参数
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON data"}), 400
        
    event_id = data.get('event_id')
    user_id = data.get('user_id')
    feedback = data.get('feedback')
    feedback_time = data.get('feedback_time') or datetime.now()
    
    if not event_id or not user_id:
        return jsonify({"error": "event_id and user_id are required"}), 400
        
    # 修改2：确保ID转换为整数类型
    try:
        event_id = int(event_id)
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": "event_id and user_id must be integers"}), 400
    
    # 如果已存在，那就报错
    might_copy = EventParticipationRecord.query.filter_by(
        event_id=event_id, 
        user_id=user_id
    ).first()
    if might_copy:
        return jsonify({"error": "This record already exists"}), 400
    
    new_record = EventParticipationRecord(
        event_id=event_id,
        user_id=user_id,
        feedback=feedback,
        feedback_time=feedback_time
    )

    try:
        db.session.add(new_record)
        db.session.commit()
        return jsonify({"message": "活动参与记录添加成功！", "id": new_record.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# 获取所有活动参与记录-支持分页
@event_participation_record_bp.route('/get_all_record', methods=['GET'])
def get_all_records():
    query = EventParticipationRecord.query
    
    # 分页参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    record_list = []
    for record in pagination.items:
        record_list.append({
            "id": record.id,
            "event_id": record.event_id,
            "user_id": record.user_id,
            "feedback": record.feedback,
            "feedback_time": record.feedback_time.strftime('%Y-%m-%d %H:%M:%S') if record.feedback_time else None
        })
    
    return jsonify({
        'records': record_list,
        'total': pagination.total,
        'pages': pagination.pages,
        'page': page,
        'per_page': per_page
    }), 200

# 获取某一用户的某个活动的参与记录
@event_participation_record_bp.route('/get_one_person_one_event_record', methods=['GET'])
def get_one_person_one_event_record():
    user_id = request.args.get('user_id')
    event_id = request.args.get('event_id')
    if not user_id or not event_id:
        return jsonify({"error": "user_id and event_id are required"}), 400
    record = EventParticipationRecord.query.filter_by(user_id=user_id, event_id=event_id).first()
    if not record:
        return jsonify({
            "state":"fail",
            "errorMsg": "活动记录没有找到"
            })
    feedback = record.feedback
    return jsonify({
        "state":"success",
        "feedback":feedback
    })

# 获取某一个用户的所有活动记录-测试正确
@event_participation_record_bp.route('/get_one_person_all_records', methods=['GET'])
def get_one_person_all_records():
    user_id = request.args.get('user_id')
    records = EventParticipationRecord.query.filter(EventParticipationRecord.user_id == user_id)
    record_list = []
    for record in records:
        record_list.append({
            "id": record.id,
            "event_id": record.event_id,
            "user_id": record.user_id,
            "feedback": record.feedback,
            "feedback_time": record.feedback_time.strftime('%Y-%m-%d %H:%M:%S') if record.feedback_time else None
        })
    return jsonify(record_list), 200

# 获取一个活动的所有参与记录-测试通过
@event_participation_record_bp.route('/get_one_event_all_records', methods=['GET'])
def get_one_event_all_records():
    event_id = request.args.get('event_id')
    records = EventParticipationRecord.query.filter(EventParticipationRecord.event_id == event_id)
    record_list = []
    for record in records:
        record_list.append({
            "id": record.id,
            "event_id": record.event_id,
            "user_id": record.user_id,
            "feedback": record.feedback,
            "feedback_time": record.feedback_time.strftime('%Y-%m-%d %H:%M:%S') if record.feedback_time else None
        })
    return jsonify(record_list), 200

# 获取单个活动参与记录-测试正确
@event_participation_record_bp.route('/<int:record_id>', methods=['GET'])
def get_single_record(record_id):
    record = EventParticipationRecord.query.get(record_id)
    if not record:
        return jsonify({"error": "活动记录没有找到"}), 404
    return jsonify({
        "id": record.id,
        "event_id": record.event_id,
        "user_id": record.user_id,
        "feedback": record.feedback,
        "feedback_time": record.feedback_time.strftime('%Y-%m-%d %H:%M:%S') if record.feedback_time else None
    }), 200

# 更新活动参与记录-测试成功
@event_participation_record_bp.route('/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    record = EventParticipationRecord.query.get(record_id)
    if not record:
        return jsonify({"error": "活动记录没有找到"}), 404

    data = request.get_json()
    event_id = data.get('event_id')
    user_id = data.get('user_id')
    feedback = data.get('feedback')

    if event_id:
        record.event_id = event_id
    if user_id:
        record.user_id = user_id
    if feedback:
        record.feedback = feedback
        record.feedback_time = datetime.now()

    try:
        db.session.commit()
        return jsonify({"message": "活动记录更新成功！"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# 这里是新增或修改评论-测试通过
@event_participation_record_bp.route('/add_or_modify_feedback', methods=['PUT'])
def add_or_modify_feedback():
    data = request.get_json()
    event_id = data.get('event_id')
    user_id = data.get('user_id')
    feedback = data.get('feedback')

    record = EventParticipationRecord.query.filter_by(event_id=event_id, user_id=user_id).first()
    if not record:
        return jsonify({"error": "活动记录没有找到,请先参与活动！"}), 404
    message = "评论新增成功！" if record.feedback is None else "评论修改成功！"

    record.feedback = feedback   # 这里需要前端保证不为空！
    record.feedback_time = datetime.now()

    try:
        db.session.commit()
        return jsonify({"message": message}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

# 删除活动参与记录
@event_participation_record_bp.route('/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    record = EventParticipationRecord.query.get(record_id)
    if not record:
        return jsonify({"error": "活动记录没有找到"}), 404

    try:
        db.session.delete(record)
        db.session.commit()
        return jsonify({"message": "活动记录删除成功！"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# 按照活动序号获取其所有参与用户的反馈
@event_participation_record_bp.route('/get_feedback_by_event', methods=['GET'])
def get_feedback_by_event():
    event_id = request.args.get('event_id')
    number = request.args.get('number') or 10
    if not event_id:
        return jsonify({"error": "event_id is required"}), 400

    # 查询总记录数
    total_count = EventParticipationRecord.query.filter(
        EventParticipationRecord.event_id == event_id
    ).count()
    
    # 查询分页记录
    records = EventParticipationRecord.query.filter(
        EventParticipationRecord.event_id == event_id
    ).limit(number).all()
    
    feedback_list = []
    for record in records:
        user = User.query.get(record.user_id)
        if user:
            feedback_list.append({
                "username": user.username,
                "comment": record.feedback
            })
    
    # 返回统一格式
    return jsonify({
        "count": total_count,
        "data": feedback_list
    }), 200

# 按照用户序号获取其所有参与活动的反馈
@event_participation_record_bp.route('/get_feedback_by_user', methods=['GET'])
def get_feedback_by_user():
    user_id = request.args.get('user_id')
    number = request.args.get('number') or 10
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    # 查询总记录数
    total_count = EventParticipationRecord.query.filter(
        EventParticipationRecord.user_id == user_id
    ).count()
    
    # 查询分页记录
    records = EventParticipationRecord.query.filter(
        EventParticipationRecord.user_id == user_id
    ).limit(number).all()
    
    feedback_list = []
    for record in records:
        event = Event.query.get(record.event_id)
        if event:
            feedback_list.append({
                "eventname": event.title,
                "feedback": record.feedback
            })
    
    # 返回统一格式
    return jsonify({
        "count": total_count,
        "data": feedback_list
    }), 200

@event_participation_record_bp.route('/get_past_events', methods=['GET'])
def get_past_events():
    # 获取活动ID列表参数，支持逗号分隔的ID字符串或JSON数组
    event_ids = request.args.get('event_ids')
    
    if not event_ids:
        return jsonify({"error": "event_ids parameter is required"}), 400

    # 解析活动ID列表
    try:
        # 尝试解析JSON数组
        if event_ids.startswith('[') and event_ids.endswith(']'):
            event_ids = json.loads(event_ids)
    except (json.JSONDecodeError, ValueError):
        return jsonify({"error": "活动id数据格式不正确"}), 401
    
    if not event_ids:
        return jsonify({"error": "没有有效的活动id"}), 402
    
    # 查询活动信息
    events = Event.query.filter(Event.id.in_(event_ids)).all()
    
    # 收集所有活动ID用于查询反馈
    event_ids_set = {event.id for event in events}
    
    # 查询这些活动的所有反馈记录
    feedback_records = EventParticipationRecord.query.filter(
        EventParticipationRecord.event_id.in_(event_ids_set)
    ).all()
    
    # 按活动ID分组反馈记录
    feedback_by_event = defaultdict(list)
    for record in feedback_records:
        user = User.query.get(record.user_id)
        if user:
            feedback_by_event[record.event_id].append({
                "user": user.username,
                "comment": record.feedback
            })
    
    # 构建响应数据
    result = []
    for event in events:
        event_data = {
            "id": event.id,
            "title": event.title,
            "organizer": event.organizer,
            "theme": event.theme,
            "date": event.start_time.strftime('%Y-%m-%d') if event.start_time else None,
            "participants": event.participate_counts,
            "evaluations": feedback_by_event.get(event.id, [])
        }
        result.append(event_data)
    
    return jsonify(result), 200