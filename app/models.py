from app import db
from datetime import datetime


class News(db.Model):
	__tablename__ = 'news'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	content = db.Column(db.Text)
	publication_date = db.Column(db.DateTime, default=datetime.utcnow)

	def to_dict(self):
		return {
			'id': self.id,
			'title': self.title,
			'content': self.content,
			'publication_date': self.publication_date.isoformat() if self.publication_date else None
		}

	def __repr__(self):
		return f'<News {self.title}>'
