#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/25 上午5:52
# @Author  : Aries
# @File    : __init__.py.py
# @Software: PyCharm
# @Email   : dewujie64@gmail.com

from flask import Flask, render_template
import pymysql
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/Video' # mysql 服务器配置
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 是否开启自动提交,如果开启会损耗服务器的资源占用
app.config['SECRET_KEY'] = '48c0e28a89d4425f83762665f546ffab' # CSRF——TOKEN 加密盐
app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads/') # 文件上传的本地磁盘地址

db = SQLAlchemy(app) # db对象 用来处理数据库 的增删改查


app.debug = True # 调试模式,线上需要关闭

from app.home import home as home_Blueprint
from app.admin import admin as admin_Blueprint


app.register_blueprint(home_Blueprint)
app.register_blueprint(admin_Blueprint, url_prefix="/admin")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html'), 404


@app.errorhandler(403)
def page_not_lonin(error):
    return render_template('home/403.html'), 403
