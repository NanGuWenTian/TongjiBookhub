from flask import Blueprint, request, jsonify
from models import db, BookCategory

book_category_bp = Blueprint('book_category', __name__, url_prefix='/api/book_category')

# 创建书籍种类-测试通过
@book_category_bp.route('', methods=['POST'])
def create_event_category():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({"error": "Name is required"}), 400

    new_category = BookCategory(name=name)
    try:
        db.session.add(new_category)
        db.session.commit()
        return jsonify({"message": f"名为{new_category.name}的书籍种类创建成功", "id": new_category.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# 获取所有书籍种类-测试通过
@book_category_bp.route('', methods=['GET'])
def get_all_book_categories():
    categories = BookCategory.query.order_by(BookCategory.id.asc()).all()
    category_list = [{"id": category.id, "name": category.name} for category in categories]
    return jsonify(category_list), 200

# 更新书籍种类-测试通过
@book_category_bp.route('/<int:category_id>', methods=['PUT'])
def update_book_category(category_id):
    category = BookCategory.query.get(category_id)
    if not category:
        return jsonify({"error": f"id为{category_id}的书籍种类没有找到"}), 404

    data = request.get_json()
    name = data.get('name')

    if name:
        category.name = name

    try:
        db.session.commit()
        return jsonify({"message": f"id为{category_id}的书籍种类成功将名字更新为{name}", "id": category.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# 删除书籍种类-测试通过
@book_category_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_book_category(category_id):
    category = BookCategory.query.get(category_id)
    if not category:
        return jsonify({"error": "书籍种类没有找到"}), 404

    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": f"名为{category.name}的书籍种类已成功删除"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500