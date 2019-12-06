#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/25 上午5:58
# @Author  : Aries
# @File    : forms.py
# @Software: PyCharm
# @Email   : dewujie64@gmail.com

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,FileField,TextAreaField,SelectField,DateField
from wtforms.validators import DataRequired, ValidationError
from app.models import User, Admin, Tag



class LoginForm(FlaskForm):
    account = StringField(label='帐号', validators=[DataRequired('请输入用户名')], description='帐号',
                          render_kw={
                              'class': "form-control",
                              'placeholder': "请输入账号！",
                              'required': 'required'
                          })
    pwd = PasswordField(label='密码', validators=[DataRequired('请输入密码')], description='密码',
                        render_kw={
                            'class': "form-control",
                            'placeholder': "请输入密码！",
                            'required': 'required'
                        })
    submit = SubmitField(label='登录', render_kw={'class': "btn btn-primary btn-block btn-flat"})

    def validate_account(self, field):
        account = field.data
        user = Admin.query.filter_by(name=account).count()
        if user == 0:
            raise ValidationError('帐号不存在')


class TagForm(FlaskForm):
    name = StringField(label='标签', validators=[DataRequired('请输入标签')], description='标签',
                       render_kw={
                           'class': "form-control",
                           'placeholder': "请输标签名称！",
                           'required': 'required'
                       })
    submit = SubmitField(label='提交', render_kw={'class': "btn btn-primary"})

    def validate_name(self, field):
        name = field.data
        tag = Tag.query.filter_by(name=name).count()
        if tag:
            raise ValidationError('名称已经存在')

class MovieForm(FlaskForm):
    title = StringField(label='片名', validators=[DataRequired('请输入片名')], description='片名',
                        render_kw={'class': "form-control",'placeholder': "请输片名！",})
    url = FileField(label='视频文件',validators=[DataRequired('请上传文件')],description='视频文件文件')
    info = TextAreaField(label='简介', validators=[DataRequired('请输入简介')], description='简介',
                        render_kw={'class': "form-control",'rows': 10, })
    logo = FileField(label='封面', validators=[DataRequired('请上传封面')], description='封面')
    start = SelectField(label='级别',validators=[DataRequired('请选择星级')],description='星级',coerce=int,
                       choices=[(1,'1星'),(2,'2星'),(3,'3星'),(4,'4星'),(5,'5星')],
                       render_kw={'class':'form-control'})
    tag_id = SelectField(label='标签',validators=[DataRequired('请选择标签')],description='标签',coerce=int,
                       choices="", render_kw={'class':'form-control'})
    area = StringField(label='地区', validators=[DataRequired('请输入地区')], description='地区',
                        render_kw={'class': "form-control",'placeholder': "请输地区！",})
    lenth = StringField(label='片长', validators=[DataRequired('请输入片长')], description='片长',
                        render_kw={'class': "form-control",'placeholder': "请输片长！",})
    release_time = DateField(label='上映时间', validators=[DataRequired('请输入上映时间')], description='上映时间',
                        render_kw={'class': "form-control",'placeholder': "上映时间",'id':'input_release_time'})
    submit = SubmitField(label='提交', render_kw={'class': "btn btn-primary"})


