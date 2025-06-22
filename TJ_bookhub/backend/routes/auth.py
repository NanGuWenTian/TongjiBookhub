from flask import Blueprint, jsonify, request
from flask_mail import Message
from app import mail, r
import random
from models import db, User
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from utils.jwt import create_access_token, create_refresh_token, refresh_access_token

authentication = Blueprint('auth', __name__, url_prefix='/api/auth')

@authentication.route('/send_captcha', methods=['POST'])
def send_captcha():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'code': 400, 'msg': '邮箱不能为空'}), 400
    
    # 限制发送频率
    cooldown_key = f'captcha:cooldown:{email}'
    if r.get(cooldown_key):
        return jsonify({'code': 429, 'msg': '请勿频繁请求验证码，稍后再试'}), 429

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
        return jsonify({'code': 500, 'msg': '邮件发送失败', 'error': str(e)}), 500


@authentication.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    captcha = data.get('captcha')

    # 参数非空校验
    if not all([username, email, password, captcha]):
        return jsonify({'code': 400, 'msg': '缺少必要参数'}), 400

    # 验证验证码
    real_code = r.get(f"captcha:{email}")
    if not real_code or real_code != captcha:
        return jsonify({'code': 400, 'msg': '验证码错误或已过期'}), 400

    # 检查用户名和邮箱是否已被注册
    if User.query.filter_by(username=username).first():
        return jsonify({'code': 400, 'msg': '用户名已存在'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'code': 400, 'msg': '邮箱已被注册'}), 400

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
        print('数据库错误:', e)  # 控制台输出
        return jsonify({'code': 500, 'msg': '数据库错误，请稍后重试'}), 500

    # 删除验证码，防止重复使用
    r.delete(f"captcha:{email}")

    return jsonify({'code': 200, 'msg': '注册成功'})


@authentication.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    account = data.get('account')
    password = data.get('password')

    if not account or not password:
        return jsonify({'code': 400, 'msg': '缺少账号或密码'}), 400

    user_username = User.query.filter_by(username=account).first()
    user_email = User.query.filter_by(email=account).first()
    if not user_email and not user_username:
        return jsonify({'code': 404, 'msg': '账号不存在'}), 404
    
    user = user_email or user_username

    if not check_password_hash(user.password, password):
        return jsonify({'code': 400, 'msg': '密码错误'}), 400
    
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    # 登录成功，返回基本信息（根据需要返回token或session）
    return jsonify({
        'code': 200,
        'msg': '登录成功',
        'data':{
            'access_token': access_token,
            'refresh_token': refresh_token,
            'is_admin': user.is_admin
        }
    })

@authentication.route('/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    refresh_token = data.get('refresh_token')

    if not refresh_token:
        return jsonify({'code': 400, 'msg': '缺少 refresh_token'}), 400

    new_token, msg = refresh_access_token(refresh_token)

    if not new_token:
        return jsonify({'code': 401, 'msg': msg}), 401

    return jsonify({'code': 200, 'access_token': new_token})