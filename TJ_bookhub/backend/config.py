import os
class Config:
    DB_USER = os.environ.get('DB_USER', 'dwbfmchpdxg')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'rZl9MEzsEPbhlZJ9')
    DB_HOST = os.environ.get('DB_HOST', 'mysql.sqlpub.com')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'tjbookhub')
    
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False