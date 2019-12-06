#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/25 上午5:58
# @Author  : Aries
# @File    : forms.py
# @Software: PyCharm
# @Email   : dewujie64@gmail.com
import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import User, Admin

class LoginForm(FlaskForm):
    account = StringField(label='帐号', validators=[DataRequired('请输入用户名')], description='帐号',
                          render_kw={
                              'placeholder': "请输入账号！",
                              'required': 'required'
                          })
    pwd = PasswordField(label='密码', validators=[DataRequired('请输入密码')], description='密码',
                          render_kw={
                              'placeholder': "请输入密码！",
                              'required': 'required'
                          })
    submit = SubmitField(label='登录',render_kw={'required': 'required'})

    def validate_account(self,field):
        account = field.data
        user = User.query.filter_by(name=account).count()
        if user == 0:
            raise ValidationError('帐号不存在')

class SignupForm(FlaskForm):
    username = StringField(label='用户名', validators=[DataRequired('请输入用户名')], description='用户名',
                          render_kw={
                              'placeholder': "请输入用户名，不能为中文！",
                              'required': 'required'
                          })
    code = StringField(label='邀请吗', validators=[DataRequired('请输入邀请码')], description='邀请码',
                        render_kw={
                            'placeholder': "请输入邀请码！",
                            'required': 'required'
                        })
    email = StringField(label='邮箱', validators=[DataRequired('请输入邮箱')], description='邮箱',
                        render_kw={
                            'placeholder': "请输入邮箱地址！",
                            'required': 'required'
                        })
    pwd = PasswordField(label='密码', validators=[DataRequired('请输入密码')], description='密码',
                        render_kw={
                            'placeholder': "请输入密码！",
                            'required': 'required'
                        })

    pwd2 = PasswordField(label='密码', validators=[DataRequired('请输入密码')], description='密码',
                          render_kw={
                              'placeholder': "请输入密码！",
                              'required': 'required'
                          })
    submit = SubmitField(label='登录',render_kw={'required': 'required'})
    a = None
    ll = ['12345']

    def validate_username(self,field):
        username = field.data
        user = User.query.filter_by(name=username).count()
        if user != 0:
            raise ValidationError('帐号已存在')

    def validate_code(self,field):
        code = field.data
        if code not in self.ll:
            raise ValidationError('请按照下方方式正确获取邀请吗')

    def validate_email(self,field):
        email = field.data
        if not re.match(u'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            raise ValidationError('请输入正确的邮箱格式:')

    def validate_pwd(self,fiedl):
        pwd = fiedl.data
        self.a = pwd

    def validate_pwd2(self,field):
        pwd2 = field.data
        if self.a != pwd2:
            raise ValidationError('两次密码不相同:')