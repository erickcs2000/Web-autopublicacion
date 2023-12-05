from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from . import db

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'), nullable=True)  
    votes = db.Column(db.Integer, default=0)  
    author = db.relationship('Users', backref='posts')
    categories = db.relationship('CategoryPost', secondary='category_post_relationship', backref=db.backref('posts', lazy='dynamic'))

class Response(db.Model):
    __tablename__ = 'response'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('response.id'), nullable=True)
    votes = db.Column(db.Integer, default=0) 
    author = db.relationship('Users', backref='responses')
    parent = db.relationship('Response', remote_side=[id], backref='children')

class VotePost(db.Model):
    __tablename__ = 'vote_post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    is_upvote = db.Column(db.Boolean, default=None)  

class VoteResponse(db.Model):
    __tablename__ = 'vote_response'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    response_id = db.Column(db.Integer, db.ForeignKey('response.id'), nullable=False)
    is_upvote = db.Column(db.Boolean, default=None)

class CategoryPost(db.Model):
    __tablename__ = 'category_post'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class CategoryPostRelationship(db.Model):
    __tablename__ = 'category_post_relationship'
    category_id = db.Column(db.Integer, db.ForeignKey('category_post.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)


