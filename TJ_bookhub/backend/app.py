from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db

def create_app():
    app = Flask(__name__)

    # 数据库配置
    app.config.from_object(Config)

    # 初始化扩展，并允许跨域访问（vue）
    db.init_app(app)
    CORS(app)

    # 创建所有表（第一次运行用）
    with app.app_context():
        db.create_all()

    # 注册蓝图
    from routes.books import books_bp
    app.register_blueprint(books_bp)
    from routes.comments import comments_bp
    app.register_blueprint(comments_bp)
    from routes.event import event_bp
    app.register_blueprint(event_bp)
    from routes.event_category import event_category_bp
    app.register_blueprint(event_category_bp)
    from routes.event_participation_record import event_participation_record_bp
    app.register_blueprint(event_participation_record_bp)


    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
