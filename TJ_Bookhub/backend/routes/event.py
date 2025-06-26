from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from models import db, Event, EventCategory

event_bp = Blueprint('events', __name__, url_prefix='/api/events')

# 创建活动-测试通过
@event_bp.route('', methods=['POST'])
def create_event():
    data = request.json
    required_fields = ['title']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    new_event = Event(
        title=data['title'],
        type_id=data.get('type_id'), #前端需要处理编号的范围问题
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
        return jsonify({"message": "活动创建成功", "id": new_event.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"创建活动时出错: {str(e)}"}), 500


# 获取活动列表-测试通过
@event_bp.route('', methods=['GET'])
def get_events():
    query = Event.query
    # query = Event.query.join(EventCategory, Event.type_id == EventCategory.id, isouter=True)
    # 这里使用 SQLAlchemy 的 join 方法执行左外连接（isouter=True），将 Event 表和 EventCategory 表关联起来

    # 获得筛选条件
    id = request.args.get('id')
    title = request.args.get('title')
    type_id = request.args.get('type_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    is_featured = request.args.get('is_featured')
    # 从里面读取participate_counts最大的
    # is_hoted = request.args.get('is_hoted')

    if id:
        query = query.filter(Event.id == id)
    if title:
        query = query.filter(Event.title.ilike(f'%{title}%'))

    if type_id:
        query = query.filter(Event.type_id == type_id)

    if start_date:
        try:
            start_date = datetime.fromisoformat(start_date)
            # 这行代码的作用是将一个符合 ISO 8601 格式的日期时间字符串转换为 Python 的 datetime 对象
            # ISO 8601的格式为 YYYY-MM-DDTHH:MM:SS
            query = query.filter(Event.start_time >= start_date)
        except ValueError:
            return jsonify({"error": "Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)."}), 400

    if end_date:
        try:
            end_date = datetime.fromisoformat(end_date)
            query = query.filter(Event.end_time <= end_date)
        except ValueError:
            return jsonify({"error": "Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)."}), 400

    if is_featured is not None: #is_featured = True or False 前端传值的时候需要注意！
        is_featured = is_featured.lower() == 'true'
        query = query.filter(Event.is_featured == is_featured)

    # 分页（修正参数传递方式）
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 8, type=int)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    # error_out=False：当请求的页码超出范围时，不会抛出错误，而是返回空列表

    event_items = []
    # bug1:!!!!!
    # 当代码执行 event.to_dict() 时，如果 Event 类没有定义 to_dict 方法，就会使用 event.__dict__。而 __dict__ 只会包含 Event 类自身的属性，不会包含关联的 EventCategory 对象的信息。
    # 就算 Event 类定义了 to_dict 方法，若该方法没有处理关联的 EventCategory 对象，同样不会包含活动类别的信息
    # for event in pagination.items:
    #     event_dict = event.to_dict() if hasattr(event, 'to_dict') else event.__dict__
    #     # 若活动对象有 to_dict 方法，就调用该方法将对象转换为字典；否则，使用 __dict__ 属性获取对象的属性字典
    #     event_dict.pop('_sa_instance_state', None)
    #     # 移除 SQLAlchemy 自动添加的 _sa_instance_state 属性，该属性包含对象的状态信息，无需返回给客户端
    #     # if  hasattr(event, 'EventCategory') and event.EventCategory:
    #     #     event_dict['category'] = {
    #     #         'id': event.EventCategory.id,
    #     #         'name': event.EventCategory.name
    #     #     }
    #     # 将类别信息加入到活动字典中
    #     event_items.append(event_dict)
    #     # 将筛选后的活动信息加入到活动列表中
    for event in pagination.items:
        event_dict = event.to_dict()
        event_dict.pop('type_id',None)
        event_items.append(event_dict)

    return jsonify({
        'event_items': event_items,
        'total': pagination.total,
        'pages': pagination.pages,
        'page': page,
        'per_page': per_page
    })

# 获取热门活动
@event_bp.route('/hot_events', methods=['GET'])
def get_hot_events():
    event_items = Event.query.order_by(Event.participate_counts.desc()).limit(4).all()
    hot_events = []
    for event in event_items:
        event_dict = event.to_dict()
        event_dict.pop('type_id',None)
        hot_events.append(event_dict)
    return jsonify({
        'code': 200,
        'message': '获取热门活动成功',
        'hot_events': hot_events
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
        return jsonify({"message": "活动更新成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"更新活动时出错: {str(e)}"}), 500

# 删除活动
@event_bp.route('/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get_or_404(id)

    try:
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "活动删除成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"删除活动时出错: {str(e)}"}), 500