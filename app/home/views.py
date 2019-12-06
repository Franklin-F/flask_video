#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/25 上午5:57
# @Author  : Aries
# @File    : views.py
# @Software: PyCharm
# @Email   : dewujie64@gmail.com
import re
from functools import wraps

from werkzeug.security import generate_password_hash

from app.home.forms import LoginForm, SignupForm
from app.models import User
from . import home
from flask import render_template, redirect, url_for, request, session, flash
from app import app,db



def admin_lonin_req(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if not session.get('admin') or session.get('admin') == None:
            return redirect(url_for("home.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_func


@home.route("/")
@admin_lonin_req
def index():
    '''
    首页
    '''
    if not session.get('admin') or session.get('admin') == None:
        return redirect(url_for("home.login", next=request.url))
    else:
        logged_in = 1
    return render_template("home/index.html",logged_in=logged_in)


@home.route("/login/", methods=["GET", "POST"])
def login():
    '''
    登录页
    '''
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data['account']).first()
        if not user.check_pwd(data['pwd']):
            flash('密码错误')
            return redirect(url_for("home.login"))
        session['admin'] = data['account']
        return redirect(request.args.get(next) or url_for("home.index"))
    return render_template('home/login.html', form=form)


@home.route("/logout/")
@admin_lonin_req
def logout():
    '''
    退出
    '''
    session.clear()
    return redirect(url_for("home.login"))


@home.route("/signup/", methods=['GET', 'POST'])
def signup():
    # 注册
    # 接收
    form = SignupForm()
    if form.validate_on_submit():
        data = form.data
        user = User(email=data['email'], pwd=generate_password_hash(data['pwd']), name=data['username'],uuid=data['code'] )
        db.session.add(user)
        db.session.commit()
        return redirect(request.args.get(next) or url_for("home.login"))
    return render_template('home/signup.html', form=form)

@home.route("/zfbzf/")
def zfbzf():
    return render_template("home/zfbzf.html")


@home.route("/wxzf/")
def wxzf():
    return render_template("home/wxzf.html")


@home.route("/wxfriend/")
def wxfriend():
    return render_template("home/wxfriend.html")


@home.route("/pwd/")
@admin_lonin_req
def pwd():
    """
    密码重置
    """
    return render_template("home/pwd.html")


#
@home.route("/moviecol/")
@admin_lonin_req
def moviecol():
    return render_template("home/moviecol.html")


@home.route("/play/")
@admin_lonin_req
def play():
    return render_template("home/video.html")
