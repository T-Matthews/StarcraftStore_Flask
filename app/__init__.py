from flask import Flask
from config import Config
app=Flask(__name__)
app.config.from_object(Config)
from . import routes
from .auth.routes import auth

#DB imports
from .models import db
from flask_migrate import Migrate
app.register_blueprint(auth)
db.init_app(app)
migrate = Migrate(app,db)


