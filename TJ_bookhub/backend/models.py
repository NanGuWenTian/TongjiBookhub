from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import Enum, func

db = SQLAlchemy()



# ****************************用户模型***************************
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now())


class UserInfo(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    phone = db.Column(db.String(20))



# ****************************图书模型***************************
class BookCategory(db.Model):
    __tablename__ = 'book_categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    publisher = db.Column(db.String(100))
    publish_date = db.Column(db.Date)
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)
    category_id = db.Column(db.Integer, db.ForeignKey('book_categories.id'), nullable=False)
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(200))
    borrow_counts = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    rating_counts = db.Column(db.Integer, default=0)


class CategoryBorrowData(db.Model):
    __tablename__ = 'category_borrow_data'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('book_categories.id')) #书籍类别
    borrow_counts = db.Column(db.Integer, default=0) 
    year = db.Column(db.Integer)
    month = db.Column(db.Integer) 

    
class BorrowRecord(db.Model):
    __tablename__ = 'borrow_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.now())
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(Enum('borrowed', 'finished', 'overdued', name='record_status'), default='borrowed')


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    


# ***************************通知模型***************************
class Noitce(db.Model):
    __tablename__ = 'notices'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)



# ***************************活动模型***************************
class EventCategory(db.Model):
    __tablename__ = 'event_categories'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('event_categories.id'))
    image = db.Column(db.String(200))  # 活动宣传图片的地址
    start_time = db.Column(db.DateTime, default = datetime.now())
    end_time = db.Column(db.DateTime, default = datetime.now() + timedelta(days=1))
    location = db.Column(db.String(200))
    brief = db.Column(db.String(500))   # 活动简介
    organizer = db.Column(db.String(200))  # 主办方
    theme = db.Column(db.String(200))     # 主题
    is_featured = db.Column(db.Boolean, default=False) # 是否为精选活动


class EventParticipationRecord(db.Model):
    __tablename__ = 'event_participation_records'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    feedback = db.Column(db.Text)
    feedback_time = db.Column(db.DateTime, default=datetime.now())

