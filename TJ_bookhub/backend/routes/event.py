from flask import Blueprint, request, jsonify
from datetime import datetime,timedelta
from models import db, Event, EventCategory

event_bp = Blueprint('events', __name__, url_prefix='/api/events')

# 创建活动
@event_bp.route('', methods=['POST'])
def create_event():
    data = request.json
    required_fields = ['title']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    new_event = Event(
        title=data['title'],
        type_id=data.get('type_id'),
        image=data.get('image'),
        start_time=data.get('start_time', datetime.now()),
        end_time=data.get('end_time', datetime.now() + timedelta(days=1)),
        location=data.get('location'),
        brief=data.get('brief'),
        organizer=data.get('organizer'),
        theme=data.get('theme'),
        is_featured=data.get('is_featured', False)
    )
    
    db.session.add(new_event)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"message": "活动创建成功，", "id为": new_event.id}), 201

# 获取活动列表
@event_bp.route('', methods=['GET'])
def get_events():
    query = Event.query
    
    # 筛选条件
    title = request.args.get('title')
    type_id = request.args.get('type_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    is_featured = request.args.get('is_featured')
    if title:
        query = query.filter(Event.title.ilike(f'%{title}%'))
    
    if type_id:
        query = query.filter(Event.type_id == type_id)
    
    if start_date:
        try:
            start_date = datetime.fromisoformat(start_date)
            query = query.filter(Event.start_time >= start_date)
        except ValueError:
            return jsonify({"error": "Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)."}), 400
    
    if end_date:
        try:
            end_date = datetime.fromisoformat(end_date)
            query = query.filter(Event.end_time <= end_date)
        except ValueError:
            return jsonify({"error": "Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)."}), 400
    
    if is_featured is not None:
        is_featured = is_featured.lower() == 'true'
        query = query.filter(Event.is_featured == is_featured)
    
    # 分页（修正参数传递方式）
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)  # 修改此行
    
    return jsonify({
        'items': [event.to_dict() for event in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'page': page,
        'per_page': per_page
    })

# 更新活动
@event_bp.route('/<int:id>', methods=['PUT'])
def update_event(id):
    event = Event.query.get_or_404(id)
    data = request.json
    
    for field in ['title', 'type_id', 'image', 'location', 'brief', 'organizer', 'theme', 'is_featured']:
        if field in data:
            setattr(event, field, data[field])
    
    if 'start_time' in data:
        try:
            event.start_time = datetime.fromisoformat(data['start_time'])
        except ValueError:
            return jsonify({"error": "Invalid start_time format. Use ISO format."}), 400
    
    if 'end_time' in data:
        try:
            event.end_time = datetime.fromisoformat(data['end_time'])
        except ValueError:
            return jsonify({"error": "Invalid end_time format. Use ISO format."}), 400
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"message": "活动更新成功"})

# 删除活动
@event_bp.route('/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get_or_404(id)
    
    try:
        db.session.delete(event)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
    return jsonify({"message": "活动删除成功"})