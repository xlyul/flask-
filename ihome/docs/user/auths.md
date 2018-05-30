### 实名认证接口

#### request 请求
    GET /user/auths/

##### params参数:
    id_name str 真实姓名
    id_card str 身份证号码

#### response 响应
##### 成功响应:
    {
        'code': 200,
        'msg': '请求成功！'
    }



#### request 请求
    PUT /user/auths/

##### params参数:
    id_name str 真实姓名
    id_card str 身份证号码

#### response 响应

##### 失败响应1:
    {
        'code': 1008,
        'msg': '身份证信息错误！'
    }
##### 失败响应2:
    {
        'code': 900,
        'msg': '数据库信息错误！'
    }
##### 失败响应3:
    {
        'code': 901,
        'msg': '参数错误！'
    }


##### 成功响应:
    {
        'code': 200,
        'msg': '请求成功！'
    }