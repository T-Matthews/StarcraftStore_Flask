#Responsible for everything database, including db tables

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created=db.Column(db.DateTime, default=datetime.utcnow())
    race = db.Column(db.String(20), nullable=False)
    minerals = db.Column(db.Integer)
    vespene = db.Column(db.Integer)
    supply = db.Column(db.Integer)
    description = db.Column(db.String(300))
    unit_tier = db.Column(db.Integer)
    unit_image = db.Column(db.String(80))
