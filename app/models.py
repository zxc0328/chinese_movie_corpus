# coding: utf-8
"""
    models.py
    ~~~~~~~~~

        数据库文件
"""
from . import db

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    year = db.Column(db.Integer)
    tags = db.Column(db.String(128))
    raw = db.Column(db.Text())
    stemmed = db.Column(db.Text())
    def __init__(self, title, year,tags,raw,stemmed):
        self.title = title
        self.year = year
        self.tags = tags
        self.raw = raw
        self.stemmed = stemmed

    def __repr__(self):
        return '<Movie %r>' % self.title

