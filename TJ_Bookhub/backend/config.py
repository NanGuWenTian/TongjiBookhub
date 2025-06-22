import os
class Config:
    DB_USER = os.environ.get('DB_USER', 'dwbfmchpdxg')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'rZl9MEzsEPbhlZJ9')
    DB_HOST = os.environ.get('DB_HOST', 'mysql.sqlpub.com')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'tjbookhub')
    
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', '476885161@qq.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'gwidqhrbdchdcbbg')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME