# coding: utf-8
from __future__ import division
from . import app,db
from flask import render_template,redirect
from flask_wtf.file import FileField
from flask_wtf import Form
from wtforms import StringField
from werkzeug import secure_filename
import jieba
from models import Movie
import nltk
from nltk import FreqDist
import re
import codecs
import jieba.analyse



class AddMovieForm(Form):
	title = StringField('电影标题')
	year = StringField('上映年份')
	tags = StringField('分类')
	body = FileField('字幕文件') 

@app.route('/', methods=('GET', 'POST'))
def upload():
    form = AddMovieForm()
    if form.validate_on_submit():
        filename = secure_filename(form.body.data.filename)
        raw = form.body.data.read()
        u = raw.decode('utf-8')
        p = re.compile(u"[\u4e00-\u9fa5]")
        l = p.findall(u)
        str = (''.join(l))
        cutted = "/".join(jieba.cut(str, cut_all=False))
        movie = Movie(form.title.data,form.year.data,form.tags.data,str,cutted)
        db.session.add(movie)
        db.session.commit()
        return redirect('/')
    else:
        filename = None
    return render_template('add_movie.html', form=form, filename=filename)

@app.route('/success')
def success():
	#seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
	return "success!!"

@app.route('/all')
def show_all():
	movies = Movie.query.all()
	length = len(movies)
	return render_template('show_all.html',movies = movies,length = length)

@app.route('/freq')
def freq():
    movies = Movie.query.all()
    all_string = '';
    for movie in movies:
        all_string += movie.stemmed;
    all_list = all_string.split('/')
    fdist = FreqDist([w for w in all_list if len(w)>9])
    common_l = fdist.most_common(300)
    return render_template('freq.html',commons = common_l)

@app.route('/lexical')
def lexical():
    keyword = "%"+"现代"+"%" 
    keyword = keyword.decode('utf-8')
    movies = Movie.query.filter(Movie.tags.like(keyword));
    all_string = '';
    for movie in movies:
        all_string += movie.stemmed;
    all_list = all_string.split('/')
    word_count = len(all_list)
    vocab_count = len(set(all_list))
    l_d = word_count/vocab_count
    return str(word_count) + " " + str(vocab_count) + " " + str(l_d)
