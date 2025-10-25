from flask import Blueprint, request, jsonify
from app.init import db
from app.models import News

news_bp = Blueprint('news', __name__, url_prefix='/api')


@news_bp.route('/news', methods=['GET'])
def get_news():
	try:
		page = request.args.get('page', 1, type=int)
		per_page = request.args.get('per_page', 10, type=int)

		if page < 1 or per_page < 1:
			return jsonify({'error': 'Page and per_page must be positive integers'}), 400

		news_pagination = News.query.paginate(
			page=page,
			per_page=per_page,
			error_out=False
		)

		return jsonify({
			'news': [item.to_dict() for item in news_pagination.items],
			'total': news_pagination.total,
			'pages': news_pagination.pages,
			'current_page': page
		})
	except Exception as e:
		return jsonify({'error': str(e)}), 500


@news_bp.route('/news/<int:id>', methods=['GET'])
def get_news_item(id):
	try:
		news_item = News.query.get_or_404(id)
		return jsonify(news_item.to_dict())
	except Exception as e:
		return jsonify({'error': str(e)}), 404


@news_bp.route('/news', methods=['POST'])
def create_news():
	try:
		data = request.get_json()

		if not data:
			return jsonify({'error': 'No JSON data provided'}), 400

		if not data.get('title'):
			return jsonify({'error': 'Title is required'}), 400

		news_item = News(
			title=data['title'],
			content=data.get('content', '')
		)

		db.session.add(news_item)
		db.session.commit()

		return jsonify(news_item.to_dict()), 201
	except Exception as e:
		db.session.rollback()
		return jsonify({'error': str(e)}), 500


@news_bp.route('/news/<int:id>', methods=['PUT'])
def update_news(id):
	try:
		news_item = News.query.get_or_404(id)
		data = request.get_json()

		if not data:
			return jsonify({'error': 'No JSON data provided'}), 400

		if not data.get('title'):
			return jsonify({'error': 'Title is required'}), 400

		news_item.title = data['title']
		news_item.content = data.get('content', '')

		db.session.commit()

		return jsonify(news_item.to_dict())
	except Exception as e:
		db.session.rollback()
		return jsonify({'error': str(e)}), 500


@news_bp.route('/news/<int:id>', methods=['DELETE'])
def delete_news(id):
	try:
		news_item = News.query.get_or_404(id)

		db.session.delete(news_item)
		db.session.commit()

		return '', 204
	except Exception as e:
		db.session.rollback()
		return jsonify({'error': str(e)}), 500
