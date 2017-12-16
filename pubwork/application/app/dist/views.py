# coding=UTF-8

import os
from flask import Blueprint, render_template, request, url_for, jsonify, redirect, session
import flask_login
from werkzeug.utils import secure_filename

myapp = Blueprint('myapp', __name__)

login_manager = flask_login.LoginManager()


# user data
users = {'ecust': {'password': 'ecust'}}


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(userid):
    if userid not in users:
        return

    user = User()
    user.id = userid
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return

    user = User()
    user.id = username
    user.is_authenticated = request.form['password'] == users[username]['password']
    return user


@myapp.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return 'Logged out'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


# 网站缺省主页
@myapp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    username = request.form['username']
    if username not in users:
        return "no such user"
    if request.form['password'] == users[username]['password']:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return redirect(url_for('myapp.updatedlog'))
    return 'Bad login'

# 登录用户首页
@myapp.route('/updatedlog')
@flask_login.login_required
def updatedlog():
    return render_template("updatedlog.html")

# react.js
@myapp.route('/react')
def react():
    return render_template("reactone.html")

# react.js
@myapp.route('/great')
def great():
    return render_template("react_two.html")

@myapp.route('/anttest')
def anttest():
    return render_template("anttest.html")