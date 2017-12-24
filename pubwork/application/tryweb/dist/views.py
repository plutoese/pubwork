# coding=UTF-8

# --------------------------------------------------------------------------------
# view文件
# @introduction: 网页路由主页面
# @dependency: WebUIDataProvider, WebDataQuerier等
# @author: plutoese
# @date: 2017.12.11
# ---------------------------------------------------------------------------------


import uuid
from flask import Blueprint, render_template, request, url_for, jsonify, redirect, session, Response
import flask_login
from werkzeug.utils import secure_filename
from .lib.utility_web_data_provider import WebUIDataProvider, WebDataQuerier
from .models import *

# 初始化
# (1) 设定网页蓝图
myapp = Blueprint('myapp', __name__)
# (2) 初始化用户注册登录管理
login_manager = flask_login.LoginManager()
# (3) 初始化用户，后期可以用Redis数据库进行管理
# ----------to be continue----------
# user data
users = {'ecust': {'password': 'ecust'}, 'plutoese':{'password':'plutoese'}}
# (4) 初始化类对象
# 网站UI的数据提供者
web_data_provider = WebUIDataProvider()
# 网站查询的数据提供者
data_querier = WebDataQuerier()


# --------------------------------
# 用户注册和登录相关类和方法
# --------------------------------

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
    return redirect(url_for('myapp.index'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

# --------------------------------
# 网站路由系统
# --------------------------------


# 网站首页
@myapp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    username = request.form['username']
    if username not in users:
        return "无此用户，请返回主页面重新登录"
    if request.form['password'] == users[username]['password']:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return redirect(url_for('myapp.user_index'))
    return '密码错误，请返回主页面重新登录！'


# 登录用户首页
@myapp.route('/user_index')
@flask_login.login_required
def user_index():
    return render_template("user_index.html",user=session['user_id'])


# 用户数据库首页
@myapp.route('/user_database')
@flask_login.login_required
def user_database():
    return render_template("user_database.html",user=session['user_id'])


# 中国城市统计数据库查询页面
@myapp.route('/city_stat_database')
@flask_login.login_required
def city_stat_database():
    return render_template("city_stat_database.html",user=session['user_id'])


# CEIC数据库查询页面
@myapp.route('/ceic_database')
@flask_login.login_required
def ceic_database():
    return render_template("ceic_database.html",user=session['user_id'])


# 我的数据集
@myapp.route('/user_dataset')
@flask_login.login_required
def user_dataset():
    return render_template("user_dataset.html",user=session['user_id'])


# --------------------------------
# 网站API数据交互和操作系统
# --------------------------------

# 网页UI数据获取的API接口
@myapp.route('/api')
def apidata():
    info = request.args.get('info')
    # 返回数据库的基本信息
    if info == 'database':
        result = web_data_provider.databse_info
        return jsonify(data=result)

    # 返回ceic数据库查询UI构建所需信息
    if info == 'ceicQuery':
        result = web_data_provider.ceic_data_query_info
        return jsonify(data=result)

    # 返回城市统计数据库查询UI构建所需信息
    if info == 'citystatquery':
        result = web_data_provider.city_stat_query_info
        return jsonify(data=result)


# 数据库查询接口
@myapp.route('/query', methods=['POST'])
def dataquery():
    if request.method == 'POST':
        query_data = request.get_json()

        if query_data['type'] == 'ceic':
            result = data_querier.ceic_query(variable=query_data['variable'], region=query_data['region'],
                                             start_year=query_data['start_year'],end_year=query_data['end_year'])

        if query_data['type'] == 'citystat':
            result = data_querier.city_stat_query(variable=query_data['variable'], region=query_data['region'],
                                                  start_year=query_data['start_year'],end_year=query_data['end_year'],
                                                  region_scale=query_data['boundary'])

        pdata = result.pop('data')
        if pdata is not None:
            filename = ''.join(['tmp',str(uuid.uuid1()),'.xlsx'])
            pdata.to_excel('./static/file/tmpfile/{}'.format(filename))
            result['saved_file'] = ''.join([request.url_root, 'static/file/tmpfile/{}'.format(filename)])
        return jsonify(data=result)


# 数据集储存操作接口
@myapp.route('/savedataset', methods=['POST'])
def savedataset():
    if request.method == 'POST':
        result = save_dataset(request.get_json())
        return jsonify(data=result)


# 数据集管理接口
@myapp.route('/datasetmanger', methods=['GET','POST'])
def datasetmanger():
    if request.method == 'GET':
        info = request.args.get('info')
        user = request.args.get('user')
        if info == 'mydataset':
            result = data_querier.dataset_query(user=user)
            return jsonify(data=result)

    if request.method == 'POST':
        operation_data = request.get_json()

        if operation_data['type'] == 'update':
            filter = {'owner':operation_data['user'], 'name':operation_data['datasetName']}
            update = {'$set': {operation_data['dataIndex']: operation_data['value']}}
            result = UserDataSet().update_one(filter=filter, update=update)
            return jsonify(data={'updated':result[operation_data['dataIndex']]})

        if operation_data['type'] == 'delete':
            filter = {'owner':operation_data['user'], 'name':operation_data['datasetName']}
            result = UserDataSet().delete_one(filter=filter)
            return jsonify(data={'deleted':result})

        if operation_data['type'] == 'toPublic':
            filter = {'owner': operation_data['user'], 'name': operation_data['datasetName']}
            update = {'$set': {'public': True}}
            result = UserDataSet().update_one(filter=filter, update=update)
            return jsonify(data={'public':result['public']})

        if operation_data['type'] == 'toPrivate':
            filter = {'owner': operation_data['user'], 'name': operation_data['datasetName']}
            update = {'$set': {'public': False}}
            result = UserDataSet().update_one(filter=filter, update=update)
            return jsonify(data={'public':result['public']})


# 数据上传
@myapp.route('/upload', methods=['POST'])
def upload_file():
    user = ''
    if request.method == 'POST':
        user = request.headers.get('User')

        if 'file' not in request.files:
            print('No file part')
            return None

        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return render_template("user_dataset.html", user=user)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if filename in os.listdir('./static/file/userfile/{}'.format(user)):
                return render_template("user_dataset.html", user=user)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            upload_dataset(owner=user, copy_from=os.path.join(UPLOAD_FOLDER, filename),
                           copy_to='./static/file/userfile/{}/{}'.format(user,filename))
            return jsonify(data='success')
            #return render_template("user_dataset.html", user=user)

    return render_template("user_dataset.html", user=user)


# --------------------------------
# 测试用的路由
# --------------------------------

"""
@myapp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    user = ''
    if request.method == 'POST':
        user = request.headers.get('User')
        print(request, request.headers.get('User'))
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return None
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return render_template("user_dataset.html", user=user)
    return render_template("user_dataset.html", user=user)
"""

# 登录用户首页
@myapp.route('/static')
def static_file():
    return redirect(''.join([request.url_root,'static/file/test.xlsx']))


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

@myapp.route('/fetch')
def fetchone():
    return render_template("fetchexample.html")

@myapp.route('/demo')
def demoweb():
    return render_template("demo02.html")

@myapp.route('/demo1')
def demoweb1():
    return render_template("demo01.html")