from flask import Blueprint, jsonify, request
from models import db, User, UserInfo
from utils.jwt import jwt_required
import os
from werkzeug.utils import secure_filename


user_bp = Blueprint('user', __name__, url_prefix='/api/user')

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



@user_bp.route('/api/upload/avatar', methods=['POST'])
def upload_avatar():
    file = request.files.get('file')
    if not file:
        return jsonify({'code': 400, 'msg': '没有文件上传'})

    filename = secure_filename(file.filename)
    filepath = os.path.join('static/avatars', filename)
    file.save(filepath)

    # 返回上传成功后的 URL
    return jsonify({'code': 200, 'url': f'/static/avatars/{filename}'})