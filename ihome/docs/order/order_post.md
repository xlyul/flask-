### 订单提交接口

#### request 请求
    POST /order/

##### params参数:
    code str 200


#### response 响应

##### 失败响应1:
    {
        'code': 901,
        'msg': '参数错误！'
    }
##### 失败响应2:
    {
        'code': 3000,
        'msg': '创建订单时间有误！'
    }
##### 失败响应3:
    {
        'code': 900,
        'msg': '数据库信息错误！'
    }

