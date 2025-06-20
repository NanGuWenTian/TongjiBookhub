from functools import wraps
from flask import request, jsonify, g

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 暂时默认有一个管理员权限用户
        return f(*args, **kwargs)
    
    return decorated_function

