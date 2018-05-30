### 客户订单处理接口

#### request 请求
    GET /order/fd/

##### params参数:
    code  str  200
    olist list 所有客户订单列表



#### request 请求
    PATCH /order/lorder/<int:id>/

##### params参数:
    code  str  200


#### response 响应

##### 失败响应1:
    {
        'code': 900,
        'msg': '数据库信息错误！'
    }

