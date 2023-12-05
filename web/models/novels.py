from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from . import db

class NovelCategory(db.Model):
    __tablename__ = 'novel_categories'
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), primary_key=True)

class NovelTag(db.Model):
    __tablename__ = 'novel_tags'
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

class LibraryBook(db.Model):
    __tablename__ = 'library_books'
    library_id = db.Column(db.Integer, db.ForeignKey('libraries.id'), primary_key=True)
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'), primary_key=True)

class Novels(db.Model):
    __tablename__ = 'novels'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    synopsis = db.Column(db.Text, nullable=False)
    cover = db.Column(db.String(255), nullable=True) # Guardamos la URL de la portada
    author_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False) # Suponiendo que tienes una tabla de usuarios
    followers = db.Column(db.Integer)
    views = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    # Relationships
    categories = db.relationship('Categories', secondary='novel_categories', back_populates='novels')
    tags = db.relationship('Tags', secondary='novel_tags', back_populates='novels')
    libraries = db.relationship('Libraries', secondary='library_books', back_populates='novels')
    
class Chapters(db.Model):
    __tablename__ = 'chapters'

    id = db.Column(db.Integer, primary_key=True)
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    number_chapter = db.Column(db.Integer, nullable=False)

    novel = db.relationship('Novels', backref=db.backref('chapters', lazy=True))

class Categories(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    novels = db.relationship('Novels', secondary='novel_categories', back_populates='categories')

class Tags(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    novels = db.relationship('Novels', secondary='novel_tags', back_populates='tags')

class Followers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'), nullable=False)
class ReadLater(db.Model):
    __tablename__ = 'read_later'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'))

    user = db.relationship('Users', backref=db.backref('read_later', cascade='all, delete-orphan'))
    novel = db.relationship('Novels', backref=db.backref('read_later', cascade='all, delete-orphan'))

class LikeNovel(db.Model):
    __tablename__ = 'like_novel'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.id'))

    user = db.relationship('Users', backref=db.backref('like_novel', cascade='all, delete-orphan'))
    novel = db.relationship('Novels', backref=db.backref('like_novel', cascade='all, delete-orphan'))

class Libraries(db.Model):
    __tablename__ = 'libraries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    # Relación con el modelo Users
    user = db.relationship('Users', back_populates='libraries')
    # Relación con el modelo Novels a través de la tabla LibraryBooks
    novels = db.relationship('Novels', secondary='library_novels', back_populates='libraries')

class LibraryNovel(db.Model):
    __tablename__ = 'library_novels'

    library_id = db.Column(db.Integer, ForeignKey('libraries.id'), primary_key=True)
    novel_id = db.Column(db.Integer, ForeignKey('novels.id'), primary_key=True)
