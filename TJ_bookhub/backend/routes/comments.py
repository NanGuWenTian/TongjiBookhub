from flask import Blueprint, jsonify, request
from models import db, Comment


comments_bp = Blueprint('comments', __name__, url_prefix='/api/comments')

@comments_bp.route('/<int:id>', methods=['GET'])
def get_comments(id):
    # 获取评论（所有用户）
    comments = Comment.query.filter_by(book_id=id) \
    .order_by(Comment.created_time.desc()) \
    .all()
    return jsonify([comment.to_dict() for comment in comments])