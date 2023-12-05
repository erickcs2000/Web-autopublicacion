from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from . import db

class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    virtual_currency_cost = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50))  
    image_path = db.Column(db.String(255))  

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)