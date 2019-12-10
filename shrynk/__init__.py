from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'N2QRzZW7OS'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shrynk.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)
admin = Admin(app)

from shrynk import routes
from shrynk.models import User,Dashboard
from shrynk.routes import MyModelView

admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Dashboard, db.session))