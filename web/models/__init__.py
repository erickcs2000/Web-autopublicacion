from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .users import Users, UserActivity
from .novels import Novels, Chapters, Categories, Tags, Followers, ReadLater, LikeNovel, Libraries, LibraryNovel, NovelCategory, NovelTag
from .posts import CategoryPost, Post, Response, VotePost, VoteResponse, CategoryPostRelationship
from .pet import Pet, Task
from .shop import Product, Purchase
from .readfiles import extract_text_from_docx, extract_text_from_pdf

