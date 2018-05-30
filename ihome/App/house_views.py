import os
import re

from flask import Blueprint, render_template, session, jsonify, request, url_for, redirect
from sqlalchemy import or_

from App.models import User, House, Area, Facility, HouseImage, Order
from utils import status_code
from utils.functions import db, is_login
from utils.settings import UPLOAD_DIR

house = Blueprint('house', __name__)


# 主页
@house.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# 主页详情
@house.route('/index/', methods=['GET'])
def index_info():
    user_name = ''
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        user_name = user.name

    houses = House.query.order_by(House.id.desc()).all()[:5]
    hlist = [house.to_dict() for house in houses]

    areas = Area.query.all()
    area_list = [area.to_dict() for area in areas]

    return jsonify(code=status_code.OK,
                   user_name=user_name,
                   hlist=hlist,
                   area_list=area_list)


# 搜索
@house.route('/search/', methods=['GET'])
def search():
    return render_template('search.html')


# 搜索页面详情
@house.route('/allsearch/', methods=['GET'])
def house_search():
    search_dict = request.args
    area_id = search_dict.get('aid')
    start_date = search_dict.get('sd')
    end_date = search_dict.get('ed')
    sort_key = search_dict.get('sk')

    houses = House.query.filter(House.area_id == area_id)

    # 对房屋houses进行处理
    # 方法一
    orders1 = Order.query.filter(Order.begin_date >= start_date, Order.end_date <= end_date)
    orders2 = Order.query.filter(Order.begin_date <= end_date, Order.end_date >= end_date)
    orders3 = Order.query.filter(Order.begin_date <= start_date, Order.end_date >= start_date)
    orders4 = Order.query.filter(Order.begin_date <= start_date, Order.end_date >= end_date)

    # 方法二
    # orders = Order.query.filter(or_(Order.begin_date <= end_date, Order.end_date >= start_date))
    orders_list1 = [o1.house_id for o1 in orders1]
    orders_list2 = [o2.house_id for o2 in orders1]
    orders_list3 = [o3.house_id for o3 in orders1]
    orders_list4 = [o4.house_id for o4 in orders1]

    orders_list = orders_list1 + orders_list2 + orders_list3 + orders_list4

    orders_list = list(orders_list)

    houses = houses.filter(House.id.notin_(orders_list))

    if sort_key:
        if sort_key == 'booking':
            sort_key = House.room_count.desc()
        if sort_key == 'price-inc':
            sort_key = House.price.asc()
        if sort_key == 'price-des':
            sort_key = House.price.desc()
    else:
        sort_key = House.id.desc()

    houses = houses.order_by(sort_key)

    hlist = [house.to_dict() for house in houses]

    areas = Area.query.all()
    area_list = [area.to_dict() for area in areas]

    return jsonify(code=status_code.OK,
                   hlist=hlist,
                   area_list=area_list)


# 我的房源页面
@house.route('/myhouse/', methods=['GET'])
@is_login
def my_house():
    return render_template('myhouse.html')


# 判断是否实名认证
@house.route('/auth_myhouse/', methods=['GET'])
@is_login
def auth_my_house():
    user = User.query.get(session['user_id'])
    if user.id_card:
        houses = House.query.filter(House.user_id == user.id).order_by(House.id.desc())
        hlist_list = []
        for h in houses:
            hlist_list.append(h.to_dict())
        return jsonify(hlist_list=hlist_list, code=status_code.OK)
    else:
        return jsonify(status_code.MYHOUSE_USER_IS_NOT_AUTH)


# 发布新房源页面
@house.route('/newhouse/', methods=['GET'])
@is_login
def new_house():
    return render_template('newhouse.html')


# 发布新房源页面所在城区与配套设施详情
@house.route('/area_facility/', methods=['GET'])
@is_login
def area_facility():
    areas = Area.query.all()
    area_list = [area.to_dict() for area in areas]

    facilities = Facility.query.all()
    facility_list = [facility.to_dict() for facility in facilities]

    return jsonify(facility_list=facility_list, area_list=area_list)


# 新房源详情提交
@house.route('/newhouse/', methods=['POST'])
@is_login
def user_new_house():
    house_dict = request.form
    house = House()
    house.user_id = session['user_id']
    house.title = house_dict.get('title')
    house.price = house_dict.get('price')
    house.area_id = house_dict.get('area_id')
    house.address = house_dict.get('address')
    house.room_count = house_dict.get('room_count')
    house.acreage = house_dict.get('acreage')
    house.unit = house_dict.get('unit')
    house.capacity = house_dict.get('capacity')
    house.beds = house_dict.get('beds')
    house.deposit = house_dict.get('deposit')
    house.min_days = house_dict.get('min_days')
    house.max_days = house_dict.get('max_days')
    facility_ids = house_dict.getlist('facility')

    if facility_ids:
        facilitys = Facility.query.filter(Facility.id.in_(facility_ids)).all()
        house.facilities = facilitys
    try:
        house.add_update()
        return jsonify(code=status_code.OK, house_id=house.id)
    except Exception as e:
        print(e)
        return jsonify(status_code.DATABASE_ERROR)


# @house.route('/posthouse/', methods=['POST'])
# def submit_new_house():
#     title = request.form.get('title')
#     price = request.form.get('price')
#     area_id = request.form.get('area_id')
#     address = request.form.get('address')
#     room_count = request.form.get('room_count')
#     acreage = request.form.get('acreage')
#     unit = request.form.get('unit')
#     capacity = request.form.get('capacity')
#     beds = request.form.get('beds')
#     deposit = request.form.get('deposit')
#     min_days = request.form.get('min_days')
#     max_days = request.form.get('max_days')
#     facilitys = request.form.getlist('facility')
#
#     user = User.query.get(session['user_id'])
#     n_house = House()
#     # n_house = House.query.filter(House.user_id == user.id)
#     n_house.user_id = user.id
#     n_house.title = title
#     n_house.price = price
#     n_house.area_id = area_id
#     n_house.address = address
#     n_house.roomcount = room_count
#     n_house.acreage = acreage
#     n_house.unit = unit
#     n_house.capacity = capacity
#     n_house.beds = beds
#     n_house.deposit = deposit
#     n_house.min_days = min_days
#     n_house.max_days = max_days
#     try:
#         n_house.add_update()
#         for facility in facilitys:
#             fac = Facility.query.filter(Facility.id == facility).first()
#             n_house.facilities.append(fac)
#             db.session.add(n_house)
#             db.session.commit()
#         return jsonify(code=status_code.OK, n_house_id=n_house.id)
#     except:
#         return jsonify(status_code.DATABASE_ERROR)

# 新房源图片提交
@house.route('/houseimages/', methods=['POST'])
@is_login
def new_house_images():
    image = request.files.get('house_image')
    house_id = request.form.get('house_id')
    if not re.match(r'^image/.*$', image.mimetype):
        return jsonify(status_code.USER_UPLOAD_IMAGE_IS_ERROR)

    # 保存图片至本地
    url = os.path.join(UPLOAD_DIR, image.filename)
    image.save(url)

    image_url = os.path.join('/static/upload/', image.filename)
    # 保存图片信息及路径至数据库
    house_image = HouseImage()
    house_image.house_id = house_id
    house_image.url = image_url
    try:
        house_image.add_update()
    except Exception as e:
        print(e)
        return jsonify(status_code.DATABASE_ERROR)

    # 我的房源主页图片展示
    house = House.query.get(house_id)
    if not house.index_image_url:
        house.index_image_url = image_url
        try:
            house.add_update()
        except Exception as e:
            print(e)
            return jsonify(status_code.DATABASE_ERROR)

    return jsonify(code=status_code.OK, image_url=image_url)


# 房源详情信息
@house.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


# 具体的一个房源信息展示
@house.route('/detail/<int:id>/', methods=['GET'])
def house_detail(id):
    house = House.query.get(id)

    booking = 1
    if 'user_id' in session:
        house.user_id = session['user_id']
        booking = 0
    return jsonify(house=house.to_full_dict(), booking=booking, code=status_code.OK)


# 订单页面
@house.route('/booking/', methods=['GET'])
@is_login
def booking():
    return render_template('booking.html')
