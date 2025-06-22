from flask import Blueprint, jsonify, request
from flask_mail import Message
from app import mail, r
import random
from models import db, User, UserInfo
from datetime import datetime
from werkzeug.security import generate_password_hash

authentication = Blueprint('auth', __name__, url_prefix='/api/auth')

@authentication.route('/send_captcha', methods=['POST'])
def send_captcha():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'code': 400, 'msg': '邮箱不能为空'})
    
    # 限制发送频率
    cooldown_key = f'captcha:cooldown:{email}'
    if r.get(cooldown_key):
        return jsonify({'code': 429, 'msg': '请勿频繁请求验证码，稍后再试'})

    # 生成验证码，存储到 Redis，设置5分钟过期
    captcha = str(random.randint(100000, 999999))
    r.setex(f'captcha:{email}', 300, captcha)

    # 设置冷却 key，有效期 60 秒
    r.setex(cooldown_key, 60, '1')

    # 发送邮件
    try:
        msg = Message(subject='【TJBookhub】验证码',
                      recipients=[email],
                      body=f'您的验证码是：{captcha}，5分钟内有效。')
        mail.send(msg)
        return jsonify({'code': 200, 'msg': '验证码已发送'})
    except Exception as e:
        return jsonify({'code': 500, 'msg': '邮件发送失败', 'error': str(e)})


@authentication.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    captcha = data.get('captcha')

    # 参数非空校验
    if not all([username, email, password, captcha]):
        return jsonify({'code': 400, 'msg': '缺少必要参数'})

    # 验证验证码
    real_code = r.get(f"captcha:{email}")
    if not real_code or real_code != captcha:
        return jsonify({'code': 400, 'msg': '验证码错误或已过期'})

    # 检查用户名和邮箱是否已被注册
    if User.query.filter_by(username=username).first():
        return jsonify({'code': 400, 'msg': '用户名已存在'})
    if User.query.filter_by(email=email).first():
        return jsonify({'code': 400, 'msg': '邮箱已被注册'})

    # 密码哈希处理
    hashed_password = generate_password_hash(password)

    # 创建新用户
    user = User(
        username=username,
        email=email,
        password=hashed_password,
        created_at=datetime.now()
    )

    # 保存到数据库
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'msg': '数据库错误，请稍后重试'})

    # 删除验证码，防止重复使用
    r.delete(f"captcha:{email}")

    return jsonify({'code': 200, 'msg': '注册成功'})