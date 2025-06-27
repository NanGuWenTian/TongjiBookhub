from flask import Blueprint, jsonify, request
from models import db, Comment, Book
from utils.jwt import jwt_required
from datetime import datetime


comments_bp = Blueprint('comments', __name__, url_prefix='/api/comments')

@comments_bp.route('/<int:id>', methods=['GET'])
@jwt_required
def get_comments(id):
    # 获取评论（所有用户）
    try:
        try:
            page = int(request.args.get('page', 1))
            limit = int(request.args.get('limit', 5))
        except ValueError:
            return jsonify({'code': 400, 'msg': '分页参数错误'}), 400
        
        pagination = Comment.query.filter_by(book_id=id).order_by(Comment.created_time.desc()).paginate(
            page=page, per_page=limit, error_out=False
        )

        comment_list = [{
            'id': c.id,
            'user_id': c.user_id,
            'content': c.content,
            'rating': c.rating,
            'created_time': c.created_time.isoformat()
        } for c in pagination.items]

        return jsonify({
            'code': 200,
            'msg': '获取评论成功',
            'data': {
                'comments': comment_list,
                'total': pagination.total
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'msg': '数据库内部错误,请稍后重试'}), 500


@comments_bp.route('/<int:id>', methods=['POST'])
@jwt_required
def add_comment(id):
    try: 
        user_id = request.user.get('user_id')
        if not user_id:
            return jsonify({'code': 404, 'msg': '用户不存在'}), 404
        
        book = Book.query.get(id)
        if not book:
            return jsonify({'code': 404, 'msg': '图书不存在'}), 404
        
        data = request.get_json().get('content')
        content = data.get('content', '').strip()
        rating = data.get('rating')

        if not content:
            return jsonify({'code': 400, 'msg': '评论内容不能为空'}), 400
        if not isinstance(rating, (int, float)) or rating < 0.5 or rating > 5:
            return jsonify({'code': 400, 'msg': '评分必须是 0.5 到 5.0 分之间的数字'}), 400

        comment = Comment(
            book_id=id,
            user_id=user_id,
            content=content,
            rating=rating,
            created_time=datetime.now()
        )
        db.session.add(comment)

        book.rating = (book.rating * book.rating_counts + rating) / (book.rating_counts + 1)
        book.rating_counts += 1
        db.session.commit()

        return jsonify({'code': 200, 'msg': '评论添加成功', 'data': {'rating': book.rating} })
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'msg': '数据库内部错误,请稍后重试'}), 500
    


@comments_bp.route('', methods=['GET'])
@jwt_required
def get_userComments():
    try: 
        user_id = request.user.get('user_id')
        if not user_id:
            return jsonify({'code': 404, 'msg': '错误！请重新登录'}), 404
        
        comments = Comment.query.filter_by(user_id=user_id).order_by(Comment.created_time.desc()).all()

        data = []
        for comment in comments:
            data.append({
                'id': comment.id,
                'book_id': comment.book_id,
                'bookTitle': comment.book.title,
                'content': comment.content,
                'rating': comment.rating,
                'date': comment.created_time.strftime('%Y-%m-%d %H:%M:%S')
            })

        return jsonify({'code': 200, 'msg': '获取评论记录成功', 'data': data})

    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'msg': '数据库内部错误,请稍后重试'}), 500
    


@comments_bp.route('/<int:id>', methods=['PUT'])
@jwt_required
def update_comment(id):
    try:        
        data = request.get_json()
        if not data:
            return jsonify({'code': 400, 'msg': '请求数据不能为空'}), 400
        
        rating = data.get('rating')
        content = data.get('content')

        if rating is None or content is None:
            return jsonify({'code': 400, 'msg': '评分和内容不能为空'}), 400

        comment = Comment.query.filter_by(id=id).first()
        if not comment:
            return jsonify({'code': 404, 'msg': '评论不存在'}), 404
        
        comment.book.rating = (comment.book.rating * comment.book.rating_counts + rating - comment.rating) / comment.book.rating_counts
        comment.rating = rating
        comment.content = content

        db.session.commit()
        return jsonify({'code': 200, 'msg': '评论修改成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'msg': '数据库内部错误,请稍后重试'}), 500
    

@comments_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required
def delete_comment(id):
    try:
        comment = Comment.query.get_or_404(id)
        if not comment:
            return jsonify({'code': 404, 'msg': '评论不存在'}), 404
        
        if comment.book.rating_counts == 1:
            comment.book.rating = 0.0
            comment.book.rating_counts = 0
        else:
            comment.book.rating = (comment.book.rating * comment.book.rating_counts - comment.rating) / (comment.book.rating_counts - 1)
            comment.book.rating_counts -= 1
            
        db.session.delete(comment)
        db.session.commit()

        return jsonify({'code': 200, 'msg': '评论删除成功'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 500, 'msg': '数据库内部错误,请稍后重试'}), 500
