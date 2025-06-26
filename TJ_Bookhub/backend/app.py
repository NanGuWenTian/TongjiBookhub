from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db
from flask_mail import Mail
import redis

mail = Mail()
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)  # decode_responses 让 redis 返回字符串

def create_app():
    app = Flask(__name__)
    # 配置
    app.config.from_object(Config)
    # 初始化扩展
    db.init_app(app)
    # 初始化邮件服务
    mail.init_app(app)
    # 允许跨域
    CORS(app)

    # 创建所有表（第一次运行用）
    # with app.app_context():
    #     db.create_all()

    # 注册蓝图
    from routes.books import books_bp
    app.register_blueprint(books_bp)

    from routes.comments import comments_bp
    app.register_blueprint(comments_bp)

    from routes.event import event_bp
    app.register_blueprint(event_bp)

    from routes.auth import authentication
    app.register_blueprint(authentication)

    from routes.event_category import event_category_bp
    app.register_blueprint(event_category_bp)

    from routes.event_participation_record import event_participation_record_bp
    app.register_blueprint(event_participation_record_bp)

    from  routes.book_category import book_category_bp
    app.register_blueprint(book_category_bp)

    from routes.user import user_bp
    app.register_blueprint(user_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
