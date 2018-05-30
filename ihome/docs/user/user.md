### 个人信息接口

#### request 请求
    GET /user/get_user_profile/

#### params参数
    user_id 用户id

#### response 响应
##### 成功响应:
    {
        'code': 200,
        'msg': '请求成功！'
    }



#### request 请求
    PUT /user/user/

##### params参数:
    name str 用户名
    avatar str 头像

#### response 响应

##### 失败响应1:
    {
        'code': 1006,
        'msg': '上传图片不符合规则！'
    }
##### 失败响应2:
    {
        'code': 900,
        'msg': '数据库信息错误！'
    }
##### 失败响应3:
    {
        'code': 1007,
        'msg': '用户已存在！'
    }
##### 失败响应4:
    {
        'code': 901,
        'msg': '参数错误！'
    }


##### 成功响应:
    {
        'code': 200,
        'msg': '请求成功！'
    }