from models import db, User, UserInfo, BookCategory, Book, CategoryBorrowData, BorrowRecord, Comment, Noitce, EventCategory, Event, EventParticipationRecord
from config import Config
from flask import Flask
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# 添加用户
def add_user():
    with app.app_context():
        user = User(username='代文波', 
                    password='123456', 
                    email='2251557@tongji.edu.cn',
                    is_admin=False,
                    created_at=datetime.now())
        db.session.add(user)
        db.session.commit()
        return user.id

# 感觉下面的数据表暂时没啥用
def add_user_info(user_id):
    with app.app_context():
        user_info = UserInfo(user_id=user_id, phone='13994310814')
        db.session.add(user_info)
        db.session.commit()

# 添加图书类别
def add_book_category():
    with app.app_context():
        category = BookCategory(name='计算机科学')
        db.session.add(category)
        db.session.commit()
        return category.id

# 添加图书
def add_book(category_id):
    with app.app_context():
        book = Book(
            title='Python编程从入门到实践',
            author='Eric Matthes',
            isbn='978-7-115-42802-8',
            publisher='人民邮电出版社',
            publish_date=datetime(2016, 7, 1),
            total_copies=5,
            available_copies=5,
            category_id=category_id,
            description='本书是一本针对所有层次的Python读者而作的Python入门书。全书分两部分：第一部分介绍用Python编程所必须了解的基本概念，包括matplotlib、NumPy和Pygal等强大的Python库和工具介绍，以及列表、字典、if语句、类、文件与异常、代码测试等内容；第二部分将理论付诸实践，讲解如何开发三个项目，包括简单的Python 2D游戏、数据可视化项目以及交互式Web应用程序。',
            cover_image='https://example.com/book_cover.jpg',
            borrow_counts=0,
            rating=0.0,
            rating_counts=0
        )
        db.session.add(book)
        db.session.commit()
        return book.id

# 添加分类借阅数据
def add_category_borrow_data(category_id):
    with app.app_context():
        data = CategoryBorrowData(
            category_id=category_id,
            borrow_counts=0,
            year=datetime.now().year,
            month=datetime.now().month
        )
        db.session.add(data)
        db.session.commit()

# 添加借阅记录
def add_borrow_record(user_id, book_id):
    with app.app_context():
        borrow_record = BorrowRecord(
            user_id=user_id,
            book_id=book_id,
            borrow_date=datetime.now(),
            due_date=datetime.now() + timedelta(days=14),
            return_date=datetime.now(),#这里先暂定为当前时间，后面归还回来再去更新
            status='borrowed'
        )
        db.session.add(borrow_record)
        db.session.commit()

# 添加书籍评论
def add_comment(user_id, book_id):
    with app.app_context():
        comment = Comment(
            user_id=user_id,
            book_id=book_id,
            content='这本书非常适合初学者，讲解详细，案例丰富。',
            rating=5,
            created_time=datetime.now()
        )
        db.session.add(comment)
        db.session.commit()

# 添加公告
def add_notice(admin_id):
    with app.app_context():
        notice = Noitce(
            admin_id=admin_id,
            title='图书馆新活动通知',
            content='为了丰富大家的阅读生活，图书馆将举办一系列读书分享会，欢迎大家踊跃参加！',
            created_time=datetime.now()
        )
        db.session.add(notice)
        db.session.commit()

# 添加活动种类
def add_event_category(category_name):
    with app.app_context():
        event_category = EventCategory(name=category_name)
        db.session.add(event_category)
        db.session.commit()
        print(f"活动类别——{category_name}已插入成功！")
        return event_category.id

# 添加活动
def add_event(event_data):
    with app.app_context():
        event = event_data
        db.session.add(event)
        db.session.commit()
        print(f"活动——{event.title}已插入成功！")
        return event.id

# 添加活动参与记录
def add_event_participation_record(event_id, user_id):
    with app.app_context():
        record = EventParticipationRecord(
            event_id=event_id,
            user_id=user_id,
            feedback='这次分享会非常有收获，学到了很多新的知识。',
            feedback_time=datetime.now()
        )
        db.session.add(record)
        db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # 添加用户
    # user_id = add_user()

    # 添加用户信息
    # add_user_info(user_id)

    # 添加图书分类
    # category_id = add_book_category()

    # 添加图书
    # book_id = add_book(category_id)

    # 添加图书借阅数据
    # add_category_borrow_data(category_id)

    # 添加图书借阅记录
    # add_borrow_record(user_id, book_id)

    # 添加添加图书评论
    # add_comment(user_id, book_id)

    # 添加通知
    # add_notice(user_id)

    # 添加活动类别
    # event_categories = ['书香雅集','传统文化','艺术展览','技术讲座','创新实践']
    # for event_category in event_categories:
    #     event_category_id = add_event_category(event_category)
    # print("添加活动类别成功!")

    # 添加活动
    # datetime.now()获取当前时间
    # timedelta(时间)表示将前面的时间加上7天
    # datetime(2025, 6, 4, 15, 30)表示指定年、月、日、时、分

    # 下面是活动模板
    # event_data = Event(
    #         title='国学经典诵读会',
    #         type_id=2,
    #         image='https://puui.qpic.cn/vpic_cover/o3365247a8l/o3365247a8l_1669686120_hz.jpg/1280',
    #         start_time=datetime(2025, 5, 25, 14, 30),
    #         end_time=datetime(2025, 5, 25, 14, 30) + timedelta(hours=1.5),
    #         location='图书馆三楼报告厅',
    #         brief='国学大师伴你诵读经典悟文化精髓',
    #         organizer='图书馆阅读推广部',
    #         theme='经典诵读',
    #         is_featured=True
    #     )
    # event_id = add_event(event_data)

    # 添加活动参与记录
    # add_event_participation_record(event_id, user_id)