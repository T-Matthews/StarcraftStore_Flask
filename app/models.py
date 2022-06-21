#Responsible for everything database, including db tables

from datetime import datetime
import email
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin
db = SQLAlchemy()
login = LoginManager()
from uuid import uuid4
from werkzeug.security import generate_password_hash

@login.user_loader
def load_user(userid):
    return User.query.get(userid)

class Units(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    race = db.Column(db.String(20), nullable=False)
    minerals = db.Column(db.Integer)
    vespene = db.Column(db.Integer)
    supply = db.Column(db.Integer)
    desc = db.Column(db.String(300))
    unit_tier = db.Column(db.Integer)
    unit_image = db.Column(db.String(200))
    url = db.Column(db.String(200))

    def __init__(self,dict):
        self.id=str(uuid4())
        self.name=dict['name'].lower()
        self.race=dict['race'].title()
        self.minerals = dict.get(['minerals'],0)
        self.vespene = dict.get(['vespene'],0)
        self.supply = dict.get(['supply'],0)
        self.desc = dict.get(['desc'],None)
        self.unit_tier= dict['tier']
        self.unit_image = dict.get(['image'],None)
        self.url = dict.get(['url'],None)

    def to_dict(self):
        return{
            "id":self.id,
            'name':self.name.title(),
            'race':self.race.title(),
            'minerals':self.minerals,
            'vespene':self.vespene,
            'supply':self.supply,
            'desc':self.desc,
            'unit_tier':self.unit_tier,
            'unit_image':self.unit_image,
            'url':self.url
        }
    def from_dict(self,dict):
        for key in dict:
            getattr(self,key)
            setattr(self,key,dict[key])

class User(db.Model, UserMixin):
    id=db.Column(db.String(40),primary_key=True)
    username = db.Column(db.String(100), nullable=False,unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password= db.Column(db.String(255),nullable=False)
    first_name =  db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.utcnow())
    api_token=db.Column(db.String(100))
 

    def __init__(self, username, email, password, first_name="",last_name=""):
        self.username = username
        self.email=email.lower()
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.id=str(uuid4())
        self.password = generate_password_hash(password)
       

