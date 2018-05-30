### 发布新房源接口

#### request 请求
    GET /user/area_facility/

#### params参数
    facility_list list 配套设施列表
    area_list  list 区域列表



#### request 请求
    POST /house/newhouse/

##### params参数:
    house_id str 新房屋id
    code str 200


#### response 响应


##### 失败响应1:
    {
        'code': 900,
        'msg': '数据库信息错误！'
    }




#### request 请求
    POST /house/newhouse/

##### params参数:
    image_url str 新房源图片
    code str 200

#### response 响应


##### 失败响应1:
    {
        'code': 1006,
        'msg': '上传图片不符合标准！'
    }

##### 失败响应2:
    {
        'code': 900,
        'msg': '数据库信息错误！'
    }

