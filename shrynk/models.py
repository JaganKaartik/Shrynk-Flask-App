from shrynk import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model,UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	urls = db.relationship('StorageMap', backref='author', lazy='dynamic')

	def __repr__(self):
		return f"User('{self.username}','{self.password}')"

class StorageMap(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
	longURL = db.Column(db.String(200),unique=True, nullable=False)
	shortURL = db.Column(db.String(100),nullable=False)
	activated = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
	expiry = db.Column(db.DateTime, nullable=True)

	def __repr__(self):
		return f"User('{self.user_id}','{self.longURL}','{self.shortURL}','{self.activated}','{self.expiry}')"