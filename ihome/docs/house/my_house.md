### 我的房源接口

#### request 请求
    GET /house/auth_myhouse/

#### params参数
    hlist_list list 我的房源列表
    code str 200


#### response 响应

##### 失败响应:
    {
        'code': 2000,
        'msg': '用户没有实名认证！'
    }
