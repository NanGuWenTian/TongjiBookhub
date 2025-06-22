import jwt
from datetime import datetime, timedelta
from flask import request, jsonify

# 配置常量
SECRET_KEY = 'your-secret-key'  # 建议改成保存在环境变量中
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_token(user_id, expires_delta, token_type):
    """生成 JWT token"""
    payload = {
        'user_id': user_id,
        'type': token_type,
        'exp': datetime.utcnow() + expires_delta,
        'iat': datetime.utcnow(),
        'nbf': datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def create_access_token(user_id):
    """生成 access token"""
    return create_token(user_id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), token_type='access')


def create_refresh_token(user_id):
    """生成 refresh token"""
    return create_token(user_id, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), token_type='refresh')


def verify_token(token):
    """验证 JWT token"""
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True, decoded
    except jwt.ExpiredSignatureError:
        return False, 'Token 已过期'
    except jwt.InvalidTokenError:
        return False, '无效的 Token'


def extract_token_from_header():
    """从请求头中提取 Bearer Token"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    parts = auth_header.split()
    if parts[0].lower() != 'bearer' or len(parts) != 2:
        return None
    return parts[1]


def jwt_required(f):
    """装饰器：验证 access token"""
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = extract_token_from_header()
        if not token:
            return jsonify({'code': 401, 'msg': '缺少或无效的 Token'}), 401

        valid, payload_or_msg = verify_token(token)
        if not valid:
            return jsonify({'code': 401, 'msg': payload_or_msg}), 401
        
        if payload_or_msg.get('type') != 'access':
            return None, '非法 token 类型'

        # 可选：将 payload 挂载到 request 上
        request.user = payload_or_msg

        return f(*args, **kwargs)

    return decorated_function


def refresh_access_token(refresh_token):
    """使用 refresh_token 刷新 access_token"""
    valid, payload_or_msg = verify_token(refresh_token)
    if not valid:
        return None, payload_or_msg
    
    if payload_or_msg.get('type') != 'refresh':
        return None, '非法 token 类型'

    new_token = create_access_token(user_id=payload_or_msg['user_id'])
    return new_token, '刷新成功'