from flask import Blueprint, jsonify, request, current_app
from models import db, User, UserInfo
from utils.jwt import jwt_required
import os
import re


user_bp = Blueprint('user', __name__, url_prefix='/api/user')

@user_bp.route('/brief', methods=['GET'])
@jwt_required
def get_userInfoBrief():
    try: 
        user_id = request.user.get('user_id')
        if not user_id:
            return jsonify({'code': 404, 'msg': '错误！请重新登录'}), 404
        
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'code': 404, 'msg': '用户不存在'}), 404
        
        user_info = UserInfo.query.filter_by(user_id=user_id).first()
        if not user_info:
            return jsonify({'code': 404, 'msg': '用户信息不存在'}), 404  
        
        return jsonify({
            'code': 200,
            'msg': '获取用户信息成功',
            'data': {
                'username': user.username,
                'email': user.email,
                'avatar': user_info.avatar
            }
        })

    except Exception as e:
        return jsonify({'code': 500, 'msg': '数据库内部错误,请稍后重试'}), 500


@user_bp.route('', methods=['GET'])
@jwt_required
def get_userInfo():
    try:
        user_id = request.user.get('user_id')
        if not user_id:
            return jsonify({'code': 404, 'msg': '错误！请重新登录'}), 404
        
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'code': 404, 'msg': '用户不存在'}), 404
        
        user_info = UserInfo.query.filter_by(user_id=user_id).first()
        if not user_info:
            return jsonify({'code': 404, 'msg': '用户信息不存在'}), 404
        
        return jsonify({
            'code': 200,
            'msg': '获取用户信息成功',
            'data': {
                'username': user.username,
                'email': user.email,
                'nickname': user_info.nickname,
                'phone': user_info.phone,
                'avatar': user_info.avatar,
                'bio': user_info.bio
            }
        })

    except Exception as e:
        return jsonify({'code': 500, 'msg': '数据库内部错误,请稍后重试'}), 500



@user_bp.route('/upload/avatar', methods=['POST'])
@jwt_required
def upload_avatar():
    file = request.files.get('avatar')
    if not file:
        return jsonify({'code': 400, 'msg': '没有文件上传'}), 400

    user_id = request.user.get('user_id')
    if not user_id:
        return jsonify({'code': 404, 'msg': '错误！请重新登录'}), 404
    
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ['.jpeg', '.png']:
        return jsonify({'code': 400, 'msg': '不支持的文件格式'}), 400
    
    filename = f"user_{user_id}{ext}"
    folder_path = os.path.join(current_app.root_path, 'static', 'uploads', 'avatars')
    os.makedirs(folder_path, exist_ok=True)
    save_path = os.path.join(folder_path, filename)
    file.save(save_path)

    avatar_url = f"/static/uploads/avatars/{filename}"

    # 返回上传成功后的 URL
    return jsonify({'code': 200, 'url': avatar_url, 'msg': '上传成功'})


@user_bp.route('/update/userInfo', methods=['PUT'])
@jwt_required
def update_userInfo():
    user_id = request.user.get('user_id')
    if not user_id:
        return jsonify({'code': 404, 'msg': '错误！请重新登录'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'code': 400, 'msg': '请求参数缺失'}), 400
    

    nickname = data.get('nickname', '').strip()
    avatar = data.get('avatar', '')
    phone = data.get('phone', '')
    email = data.get('email', '').strip()
    bio = data.get('bio', '')

    if not nickname:
        return jsonify({'code': 400, 'msg': '昵称不能为空'}), 400
    
    if not email:
        return jsonify({'code': 400, 'msg': '邮箱不能为空'}), 400
    
    if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({'code': 400, 'msg': '邮箱格式不正确'}), 400
    
    if phone and not re.match(r"^[0-9\-+]{0,20}$", phone):
        return jsonify({'code': 400, 'msg': '电话号码格式不正确'}), 400

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'code': 404, 'msg': '用户不存在'}), 404
    
    user_info = UserInfo.query.filter_by(user_id=user_id).first()
    if not user_info:
        return jsonify({'code': 404, 'msg': '用户信息不存在'}), 404
    
    user.email = email
    user_info.nickname = nickname
    user_info.phone = phone
    user_info.bio = bio

    if avatar:
        user_info.avatar = avatar

    try:
        db.session.commit()
        return jsonify({'code': 200, 'msg': '用户信息更新成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'msg': f'更新失败: {str(e)}'}), 500

    
    