from datetime import datetime

from flask import Blueprint, request, jsonify, session, render_template

from App.models import Order, House
from utils import status_code
from utils.functions import is_login

order = Blueprint('order', __name__)


# 订单提交
@order.route('/', methods=['POST'])
@is_login
def orders():
    order_dict = request.form

    house_id = order_dict.get('house_id')
    start_time = order_dict.get('start_time')
    end_time = order_dict.get('end_time')
    if start_time and end_time:
        start_time = datetime.strptime(order_dict.get('start_time'), '%Y-%m-%d')
        end_time = datetime.strptime(order_dict.get('end_time'), '%Y-%m-%d')

        if Order.query.all():
            order = Order.query.filter(Order.house_id==house_id).first()
            if order.end_date < start_time or order.begin_date > start_time:
                start_time = start_time
                end_time = end_time
            else:
                start_time = ''
                end_time = ''
    else:
        start_time = start_time
        end_time = end_time

    if not all([house_id, start_time, end_time]):
        return jsonify(status_code.PARAMS_ERROT)

    if start_time > end_time:
        return jsonify(status_code.ORDER_START_TIME_GT_END_TIME)

    house = House.query.get(house_id)

    order = Order()
    order.user_id = session['user_id']
    order.house_id = house_id
    order.begin_date = start_time
    order.end_date = end_time
    order.house_price = house.price
    order.days = (end_time - start_time).days + 1
    order.amount = order.days * order.house_price

    try:
        order.add_update()
        return jsonify(code=status_code.OK)
    except:
        return jsonify(status_code.DATABASE_ERROR)


# 订单
@order.route('/order/', methods=['GET'])
@is_login
def orderes():
    return render_template('orders.html')


# 所有订单
@order.route('/allorders/', methods=['GET'])
@is_login
def all_orders():
    user_id = session['user_id']
    orders = Order.query.filter(Order.user_id == user_id)
    order_list = [order.to_dict() for order in orders]
    return jsonify(code=status_code.OK, order_list=order_list)


# 客户订单
@order.route('/lorder/', methods=['GET'])
@is_login
def lorder():
    return render_template('lorders.html')


# 客户订单详情
@order.route('/fd/', methods=['GET'])
@is_login
def lorders_fd():
    # 第一种方式
    # 先查询房东房屋的id
    houses = House.query.filter(House.user_id == session['user_id'])
    houses_ids = [house.id for house in houses]

    # 通过房屋的id去查找订单
    orders = Order.query.filter(Order.house_id.in_(houses_ids)).order_by(Order.id.desc())
    olist = [order.to_dict() for order in orders]

    # 第二种方式：
    # houses = House.query.filter(House.user_id == session['user_id'])
    # olist = []
    # for house in houses:
    #     orders = house.orders
    #     order_list.append(orders)
    return jsonify(olist=olist, code=status_code.OK)


# 客户订单确认
@order.route('/lorder/<int:id>/', methods=['PATCH'])
@is_login
def order_status(id):
    status = request.form.get('status')
    order = Order.query.get(id)
    order.status = status
    if status == 'REJECTED':
        comment = request.form.get('comment')
        order.comment = comment
    try:
        order.add_update()
        return jsonify(code=status_code.OK)
    except:
        return jsonify(status_code.DATABASE_ERROR)
