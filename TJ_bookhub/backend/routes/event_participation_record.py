from flask import Blueprint, request, jsonify
from models import db, EventParticipationRecord
from datetime import datetime

event_participation_record_bp = Blueprint('event_participation_record', __name__, url_prefix='/api/event_participation_record')

# 创建活动参与记录
@event_participation_record_bp.route('/', methods=['POST'])
def create_record():
    data = request.get_json()
    event_id = data.get('event_id')
    user_id = data.get('user_id')
    feedback = data.get('feedback')

    if not event_id or not user_id:
        return jsonify({"error": "event_id and user_id are required"}), 400

    new_record = EventParticipationRecord(
        event_id=event_id,
        user_id=user_id,
        feedback=feedback
    )

    try:
        db.session.add(new_record)
        db.session.commit()
        return jsonify({"message": "Record created successfully", "id": new_record.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# 获取所有活动参与记录
@event_participation_record_bp.route('/', methods=['GET'])
def get_all_records():
    records = EventParticipationRecord.query.all()
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

# 获取单个活动参与记录
@event_participation_record_bp.route('/<int:record_id>', methods=['GET'])
def get_single_record(record_id):
    record = EventParticipationRecord.query.get(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404
    return jsonify({
        "id": record.id,
        "event_id": record.event_id,
        "user_id": record.user_id,
        "feedback": record.feedback,
        "feedback_time": record.feedback_time.strftime('%Y-%m-%d %H:%M:%S') if record.feedback_time else None
    }), 200

# 更新活动参与记录
@event_participation_record_bp.route('/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    record = EventParticipationRecord.query.get(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404

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
        return jsonify({"message": "Record updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# 删除活动参与记录
@event_participation_record_bp.route('/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    record = EventParticipationRecord.query.get(record_id)
    if not record:
        return jsonify({"error": "Record not found"}), 404

    try:
        db.session.delete(record)
        db.session.commit()
        return jsonify({"message": "Record deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500