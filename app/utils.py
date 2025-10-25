import json
from datetime import datetime
from app import db
from app.models import News


def try_load_initial_data(file_path='resources/initial_data.json'):
	try:
		with open(file_path, 'r', encoding='utf-8') as f:
			data = json.load(f)

		for item in data:
			existing_news = News.query.filter_by(title=item['title']).first()
			if not existing_news:
				news = News(
					title=item['title'],
					content=item['content'],
					publication_date=datetime.fromisoformat(item['publication_date'])
				)
				db.session.add(news)

		db.session.commit()
		print(f'Successfully loaded {len(data)} records from {file_path}')
		return True
	except Exception as e:
		print(f'Error while loading initial data: {e}')
		db.session.rollback()
		return False
