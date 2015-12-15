# coding: utf-8
from flask import render_template,redirect
from . import app
from flask_wtf import Form
from wtforms import StringField
from werkzeug import secure_filename
from flask_wtf.file import FileField
import jieba
from models import Movie
import nltk
from nltk import FreqDist

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
        #form.body.data.save('uploads/' + filename)
        raw = form.body.data.read()
        cutted = "/ ".join(jieba.cut(raw, cut_all=True))
        movie = Movie(form.title.data,form.year.data,form.tags.data,raw,cutted)
        db.session.add(movie)
        db.session.commit()
        return redirect('/all')
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
	fdist = FreqDist([w for w in all_list])
	common_l = fdist.most_common(300)
	return render_template('freq.html',commons = common_l)