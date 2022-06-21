from flask import Flask
from config import Config
app=Flask(__name__)
app.config.from_object(Config)
from . import routes
from .auth.routes import auth
from .api.routes import api

#DB imports
from .models import db, login
from flask_migrate import Migrate
app.register_blueprint(auth)

db.init_app(app)
migrate = Migrate(app,db)


#setup login manager
login.init_app(app)
login.login_view = 'auth.login'
login.login_message = 'Please log in to see this page.'
login.login_message_category = 'danger'


app.register_blueprint(api)

