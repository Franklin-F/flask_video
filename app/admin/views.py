#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/25 上午5:57
# @Author  : Aries
# @File    : views.py
# @Software: PyCharm
# @Email   : dewujie64@gmail.com
from app.models import User, Admin, Tag, Movie
from . import admin
from flask import render_template, redirect, url_for, request, flash, session
from app.admin.forms import LoginForm, TagForm, MovieForm
from functools import wraps
from app import db, app
from werkzeug.utils import secure_filename
import os
import uuid
import datetime


def admin_lonin_req(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if not session.get('admin') or session.get('admin') == None:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_func


def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%s') + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


@admin.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = Admin.query.filter_by(name=data['account']).first()
        if not user.check_pwd(data['pwd']):
            flash('密码错误')
            return redirect(url_for("admin.login"))
        session['admin'] = data['account']
        return redirect(request.args.get(next) or url_for("admin.index"))
    return render_template('admin/login.html', form=form)


@admin.route("/")
@admin_lonin_req
def index():
    return render_template('admin/index.html')


@admin.route("/logout/")
@admin_lonin_req
def logout():
    session.clear()
    return redirect(url_for('admin.login'))


@admin.route("/pwd/")
@admin_lonin_req
def pwd():
    return render_template('admin/pwd.html')


@admin.route("/tag/add/", methods=["GET", "POST"])
@admin_lonin_req
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag(name=data['name'], )
        db.session.add(tag)
        db.session.commit()
        flash('添加成功可以继续添加')
        return redirect(url_for('admin.tag_add'))
    return render_template('admin/tag_add.html', form=form)


@admin.route("/tag/list/<int:page>/", methods=["GET"])
@admin_lonin_req
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(-Tag.id.desc()).paginate(page=page, per_page=10)
    return render_template('admin/tag_list.html', page_data=page_data)


@admin.route("/tag/del/<int:id>/", methods=["GET"])
@admin_lonin_req
def tag_del(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash('删除成功')
    return redirect(url_for('admin.tag_list', page=1))


@admin.route("/movie/list/<int:page>", methods=["GET", "POST"])
@admin_lonin_req
def movie_list(page=None):
    if page is None:
        page = 1
    page_data = Movie.query.filter(Tag.id==Movie.tag_id).order_by(-Movie.id.desc()).paginate(page=page, per_page=10)
    return render_template('admin/movie_list.html',page_data=page_data)


@admin.route("/movie/add/", methods=["GET", "POST"])
@admin_lonin_req
def movie_add():
    form = MovieForm()
    if request.method == "GET":
        form.tag_id.choices = [(v.id, v.name) for v in Tag.query.all()]
    if request.method == 'POST':
        form.tag_id.choices = [(int(v.id), v.name) for v in Tag.query.all()]
        if form.validate_on_submit():
            data = form.data
            file_url = secure_filename(form.url.data.filename)
            file_logo = secure_filename(form.logo.data.filename)
            if not os.path.exists(app.config["UP_DIR"]):
                os.makedirs(app.config['UP_DIR'])
                os.chmod(app.config['UP_DIR'], "rw")
            url = change_filename(file_url)
            logo = change_filename(file_logo)

            form.url.data.save(app.config['UP_DIR'] + url)
            form.logo.data.save(app.config['UP_DIR'] + logo)

            movie = Movie(
                title=data['title'],
                url=url,
                info=data['info'],
                logo=logo,
                start=int(data['start']),
                playnum=0,
                commentunm=0,
                tag_id=int(data['tag_id']),
                area=data['area'],
                release_time=data['release_time'],
                lenth=data['lenth'],
            )
            db.session.add(movie)
            db.session.commit()
            flash('添加成功！，可继续添加')
            return redirect(url_for('admin.movie_add'))
    return render_template('admin/movie_add.html', form=form)
