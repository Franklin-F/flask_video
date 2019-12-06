#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/25 上午5:57
# @Author  : Aries
# @File    : __init__.py.py
# @Software: PyCharm
# @Email   : dewujie64@gmail.com
from flask import Blueprint

home = Blueprint("home", __name__)

import app.home.views