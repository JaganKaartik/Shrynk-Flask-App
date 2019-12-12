from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_admin import Admin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'N2QRzZW7OS'
app.config['DATABASE_URL'] = 'postgres://etxpofekipqloy:736260567557fc1973cff43667da107d83a69415651a441ae79d00158bd1e8fe@ec2-174-129-255-11.compute-1.amazonaws.com:5432/d74uieftmai00v'
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