from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import Enum, func

db = SQLAlchemy()



# ****************************用户模型***************************
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user_info = db.relationship(
        'UserInfo',
        backref='user',
        cascade='all, delete',
        passive_deletes=True,
        uselist=False
    )

    comments = db.relationship(
        'Comment',
        backref='user',
        cascade='all, delete',
        passive_deletes=True
    )

    borrow_records = db.relationship(
        'BorrowRecord',
        backref='user',
        cascade='all, delete',
        passive_deletes=True
    )


class UserInfo(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    nickname = db.Column(db.String(50))
    avatar = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    bio = db.Column(db.Text)



# ****************************图书模型***************************
class BookCategory(db.Model):
    __tablename__ = 'book_categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    books = db.relationship(
        'Book',
        backref='category',
        cascade='all, delete',
        passive_deletes=True
    )

    category_borrow_data = db.relationship(
        'CategoryBorrowData',
        backref='category',
        cascade='all, delete',
        passive_deletes=True
    )



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
    category_id = db.Column(db.Integer, db.ForeignKey('book_categories.id', ondelete='CASCADE'), nullable=False)
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(200))
    borrow_counts = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    rating_counts = db.Column(db.Integer, default=0)

    borrow_records = db.relationship(
        'BorrowRecord',
        backref='book',
        cascade='all, delete',
        passive_deletes=True
    )

    comments = db.relationship(
        'Comment',
        backref='book',
        cascade='all, delete',
        passive_deletes=True
    )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'publisher': self.publisher,
            'publish_date': self.publish_date,
            'total_copies': self.total_copies,
            'available_copies': self.available_copies,
            'category': self.category_id,
            'description': self.description,
            'cover_image': self.cover_image,
            'borrow_counts': self.borrow_counts,
            'rating': self.rating,
            'rating_counts': self.rating_counts
        }


class CategoryBorrowData(db.Model):
    __tablename__ = 'category_borrow_data'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('book_categories.id', ondelete='CASCADE')) #书籍类别
    borrow_counts = db.Column(db.Integer, default=0) 
    year = db.Column(db.Integer)
    month = db.Column(db.Integer) 

    
class BorrowRecord(db.Model):
    __tablename__ = 'borrow_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.now)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(Enum('borrowed', 'finished', 'overdued', name='record_status'), default='borrowed')


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.now, nullable=False)


# ***************************通知模型***************************
class Noitce(db.Model):
    __tablename__ = 'notices'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.now, nullable=False)



# ***************************活动模型***************************
class EventCategory(db.Model):
    __tablename__ = 'event_categories'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # 补充一个连接关系
    events = db.relationship('Event', backref='category',lazy=True)
    # backref 是一个反向引用，它允许你从 Event 类的实例中访问关联的 EventCategory 实例
    # 在 Event 类的实例中会自动添加一个名为 category 的属性，通过这个属性可以访问与之关联的 EventCategory 实例
    # lazy 参数控制关联对象的加载方式。表示采用延迟加载（Lazy Loading）策略


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('event_categories.id'))
    image = db.Column(db.String(200))  # 活动宣传图片的地址
    start_time = db.Column(db.DateTime, default = datetime.now)
    end_time = db.Column(db.DateTime, default = lambda: datetime.now() + timedelta(days=1))
    location = db.Column(db.String(200))
    brief = db.Column(db.String(500))   # 活动简介
    organizer = db.Column(db.String(200))  # 主办方
    theme = db.Column(db.String(200))     # 主题
    is_featured = db.Column(db.Boolean, default=False) # 是否为精选活动
    participate_counts = db.Column(db.Integer, default=0)

    # 转换成字典
    def to_dict(self):
        event_dict = {
            'id': self.id,
            'title': self.title,
            'type_id': self.type_id,
            'image': self.image,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'location': self.location,
            'brief': self.brief,
            'organizer': self.organizer,
            'theme': self.theme,
            'is_featured': self.is_featured,
            'participate_counts': self.participate_counts
        }
        # 处理关联的活动种类信息
        if self.category:
            event_dict['category'] = {
                'id': self.category.id,
                'name': self.category.name
            }
        return event_dict

class EventParticipationRecord(db.Model):
    __tablename__ = 'event_participation_records'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    feedback = db.Column(db.Text)
    feedback_time = db.Column(db.DateTime, default=datetime.now)

