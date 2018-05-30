import os
import re

from flask import Blueprint, render_template, request, jsonify, session, redirect

from App.models import db, User
from utils import status_code
from utils.settings import UPLOAD_DIR
from utils.functions import is_login

user = Blueprint('user', __name__)


@user.route('/createdb/')
@is_login
def create_db():
    db.create_all()
    return '创建数据库成功！'


# 注册页面
@user.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


# 注册提交
@user.route('/register/', methods=['POST'])
def user_register():
    register_dict = request.form
    mobile = register_dict.get('mobile')
    password = register_dict.get('password')
    password2 = register_dict.get('password2')

    if not all([mobile, password, password2]):
        return jsonify(status_code.USER_REGISTER_PARAMS_ERROR)

    if not re.match(r'^1[345789]\d{9}$', mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)

    if User.query.filter(User.phone == mobile).count():
        return jsonify(status_code.USER_REGISTER_MOBILE_IS_EXSITS)

    if password != password2:
        return jsonify(status_code.USER_REGISTER_PASSWORD_IS_ERROR)

    us = User()
    us.phone = mobile
    us.name = mobile
    us.password = password
    try:
        us.add_update()
        return jsonify(status_code.SUCCESS)
    except Exception as e:
        print(e)
        return jsonify(status_code.DATABASE_ERROR)


# 登陆
@user.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


# 登陆提交
@user.route('/login/', methods=['POST'])
def user_login():
    user_dict = request.form
    mobile = user_dict.get('mobile')
    password = user_dict.get('password')

    if not all([mobile, password]):
        return jsonify(status_code.PARAMS_ERROT)
    if not re.match(r'^1[345789]\d{9}$', mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)
    us = User.query.filter(User.phone == mobile).first()
    if us:
        if us.check_pwd(password):
            session['user_id'] = us.id
            return jsonify(status_code.SUCCESS)
        else:
            return jsonify(status_code.USER_LOGIN_PASSWORD_IS_ERROR)
    else:
        return jsonify(status_code.USER_LOGIN_IS_NOT_EXIST)


# 个人中心
@user.route('/my/', methods=['GET'])
@is_login
def my():
    return render_template('my.html')


# 个人信息
@user.route('/user/', methods=['GET'])
@is_login
def get_user_profile():
    user_id = session['user_id']
    us = User.query.get(user_id)
    return jsonify(user=us.to_basic_dict(), code='200')


# 修改页面
@user.route('/profile/', methods=['GET'])
@is_login
def profile():
    return render_template('profile.html')


# 修改操作
@user.route('/user/', methods=['PUT'])
@is_login
def user_profile():
    user_dict = request.form
    file_dict = request.files
    if 'avatar' in file_dict:
        f1 = file_dict.get('avatar')
        # 判断是否为图片类型
        if not re.match(r'^image/.*$', f1.mimetype):
            return jsonify(status_code.USER_UPLOAD_IMAGE_IS_ERROR)
        url = os.path.join(UPLOAD_DIR, f1.filename)
        f1.save(url)

        us = User.query.filter(User.id == session['user_id']).first()
        image_url = os.path.join('/static/upload/', f1.filename)
        us.avatar = image_url
        try:
            us.add_update()
            return jsonify(code=status_code.OK, url=image_url)
        except Exception as e:
            print(e)
            return jsonify(status_code.DATABASE_ERROR)
    elif 'name' in user_dict:
        name = user_dict.get('name')
        if User.query.filter(User.name == name).count():
            return jsonify(status_code.USER_UPLOAD_USERNAME_IS_EXIST)
        us = User.query.get(session['user_id'])
        us.name = name
        try:
            us.add_update()
            return jsonify(status_code.SUCCESS)
        except Exception as e:
            print(e)
            return jsonify(status_code.DATABASE_ERROR)
    else:
        return jsonify(status_code.PARAMS_ERROT)


# 实名认证页面
@user.route('/auth/', methods=['GET'])
@is_login
def auth():
    return render_template('auth.html')


# 实名认证信息展示
@user.route('/auths/', methods=['GET'])
@is_login
def get_user_auth():
    us = User.query.get(session['user_id'])
    if all([us.id_card, us.id_name]):
        return jsonify(code=status_code.OK,
                       id_name=us.id_name,
                       id_card=us.id_card)
    else:
        return redirect('/user/auth/')


# 实名认证操作
@user.route('/auths/', methods=['PUT'])
@is_login
def auth_check():
    id_name = request.form.get('id_name')
    id_card = request.form.get('id_card')
    if not all([id_name, id_card]):
        return jsonify(status_code.PARAMS_ERROT)
    if not re.match(r'^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}([0-9]|X)$', id_card):
        return jsonify(status_code.USER_AUTH_IDCARD_IS_ERROR)
    try:
        us = User.query.get(session['user_id'])
        us.id_card = id_card
        us.id_name = id_name

        us.add_update()
        return jsonify(status_code.SUCCESS)
    except Exception as e:
        print(e)
        return jsonify(status_code.DATABASE_ERROR)


# 退出
@user.route('/logout/')
@is_login
def user_logout():
    session.clear()
    return jsonify(status_code.SUCCESS)
