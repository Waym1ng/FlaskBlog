from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    user_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    pwd = db.Column(db.String(255),nullable=False)
    __tablename__ = 'user'

    def save(self):
        db.session.add(self)
        db.session.commit()


class Category(db.Model):

    c_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    c_name = db.Column(db.String(50),unique=True,nullable=False)
    # 别名
    alias = db.Column(db.String(50),unique=True,nullable=True)
    arts = db.relationship('Article',backref='category',lazy=True)

    __tablename__ = 'category'


class Article(db.Model):
    a_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(50),unique=True,nullable=False)
    desc = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    type = db.Column(db.Integer,db.ForeignKey('category.c_id'),nullable=True)

