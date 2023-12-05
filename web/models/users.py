from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from . import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_profile = db.Column(db.String(255), nullable=True)
    bg_color = db.Column(db.String(7), default='#FFFFFF')
    description = db.Column(db.Text, nullable=True)
    libraries = db.relationship('Libraries', back_populates='user')
    virtual_currency = db.Column(db.Integer, default=0)
    user_purchases = db.relationship('Purchase', backref='user', lazy=True)
    user_pets = db.relationship('Pet', backref='user', lazy=True)

class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    activity_type = db.Column(db.String(50)) 
    quantity = db.Column(db.Integer) 
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)