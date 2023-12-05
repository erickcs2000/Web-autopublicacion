from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from . import db
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, default=1)
    experience = db.Column(db.Integer, default=0)
    type = db.Column(db.String(100)) 
    active = db.Column(db.Boolean, default=False)  

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    virtual_currency_reward = db.Column(db.Integer, nullable=False)
    task_type = db.Column(db.String(50))  
    requirement = db.Column(db.Integer)  