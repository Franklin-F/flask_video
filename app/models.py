#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/25 上午5:53
# @Author  : Aries
# @File    : models.py
# @Software: PyCharm
# @Email   : dewujie64@gmail.com

import datetime

from app.exts import db


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.String(100), unique=True)
    face = db.Column(db.String(255))  # 头像地址
    addtime = db.Column(db.DATETIME, index=True, default=datetime.datetime.now())
    uuid = db.Column(db.String(255))  # 标识符
    userlogs = db.relationship('Userlog', backref='user')
    comments = db.relationship('Comment', backref='user')  # 评论外键关联
    moviecols = db.relationship('Moviecol', backref='user')  # 评论外键关联

    def __repr__(self):
        return "<User %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


class Userlog(db.Model):
    __tablename__ = 'userlog'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))  # 所属会员，关联用户表
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DATETIME, index=True, default=datetime.datetime.now())

    def __repr__(self):
        return "<Userlog %r>" % self.id


# 标签
class Tag(db.Model):
    __tablename__ = 'tag'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)  # id
    name = db.Column(db.String(100), unique=True)  # 标签标题
    image = db.Column(db.String(255))
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now())
    movies = db.relationship("Movie", backref="tag")  # 电影外键

    def __repr__(self):
        return "<Tag %r>" % self.name


# 电影
class Movie(db.Model):
    __tablename__ = 'movie'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)  # id
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)
    logo = db.Column(db.String(255), unique=True) # 封面
    start = db.Column(db.SmallInteger)  # 星级级别
    playnum = db.Column(db.BigInteger)  # 播放量
    commentunm = db.Column(db.BigInteger)  # 评论数
    tag_id = db.Column(db.Integer, db.ForeignKey(Tag.id))  # 分类
    area = db.Column(db.String(255))  # 地区
    release_time = db.Column(db.Date)  # 上映时间
    lenth = db.Column(db.String(100))  # 电影长度
    addtime = db.Column(db.DateTime, index=True, default=datetime.datetime.now())  # 添加时间
    commens = db.relationship("Comment", backref="movie")  # 评论关联
    moviecols = db.relationship("Moviecol", backref="movie")  # 评论关联

    def __repr__(self):
        return "<Movie %r>" % self.title


# 上映预告
class Preview(db.Model):
    __tablename__ = 'preview'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)  # id
    title = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DATETIME, index=True, default=datetime.datetime.now())  # 添加时间

    def __repr__(self):
        return "<Preview %r>" % self.title


# 评论表
class Comment(db.Model):
    __tablename__ = 'comment'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)  # id
    comment = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey(Movie.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))  # 所属用户
    addtime = db.Column(db.DATETIME, index=True, default=datetime.datetime.now())  # 添加时间

    def __repr__(self):
        return "<Comment %r>" % self.id


# 收藏
class Moviecol(db.Model):
    __tablename__ = 'moviecol'
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)  # id
    comment = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey(Movie.id))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))  # 所属用户
    addtime = db.Column(db.DATETIME, index=True, default=datetime.datetime.now())  # 添加时间

    def __repr__(self):
        return "<Moviecol %r>" % self.id


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)  # id
    name = db.Column(db.String(100), unique=True)  # 标签标题
    url = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DATETIME, index=True, default=datetime.datetime.now())

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色
class Role(db.Model):
    __tablename__ = "role"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)  # 标签标题
    auths = db.Column(db.String(600))
    addtime = db.Column(db.DATETIME, index=True, default=datetime.datetime.now())
    admins = db.relationship("Admin", backref='role')

    # oplogs = db.relationship("Oplog", backref='role')

    def __repr__(self):
        return "<Role %r>" % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)  #
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.SmallInteger)
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id))
    addtime = db.Column(db.DATETIME, index=True, default=datetime.datetime.now())
    adminlogs = db.relationship("Adminlog", backref='admin')

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 管理员登录
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey(Admin.id))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DATETIME, index=True, default=datetime.datetime.now())

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 后台操作
class Oplog(db.Model):
    __tablename__ = "oplog"

    __table_args__ = {"extend_existing": True}
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey(Admin.id))
    ip = db.Column(db.String(100))
    reson = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DATETIME, index=True, default=datetime.datetime.now())

    def __repr__(self):
        return "<Oplog %r>" % self.id


if __name__ == '__main__':

    db.drop_all()
    db.create_all()
