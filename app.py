#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/25 上午5:35
# @Author  : Aries
# @File    : app.py
# @Software: PyCharm
# @Email   : dewujie64@gmail.com

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "<h1 style='color:red'>hello</h1>"


if __name__ == '__main__':
    app.run()