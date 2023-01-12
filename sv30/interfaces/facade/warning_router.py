import ast
from fastapi import APIRouter
from interfaces.assembler.str_to_data import string_to_date
from application.service.warning_service import warning_date, warning_message, warning_number, update_limit, \
    update_unread, get_limit
from interfaces.assembler.des import des_en, des_de
router = APIRouter()


@router.get('/warning_message', name='获取未读异常信息')
def get_warning_message(page, size):
    """
        获取未读异常信息
        ---
        # 参数信息
        |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
        |       ---- | ---- | ---- | ---- | ---- |
        |   page     | int | 页码 | 是 | |
        |   size     | int | 展示数量 | 是 | |
    """
    page, size = int(des_de(page)), int(des_de(size))
    data = warning_message(page, size)
    return_data = {'data': data, 'comment': '未读异常信息', 'code': 1}
    des_data = des_en(return_data)
    return des_data


@router.get('/warning_number', name='获取未读异常次数')
def get_warning_number():
    """
        获取未读异常次数
        ---
        # 参数信息
        |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
        |       ---- | ---- | ---- | ---- | ---- |
    """
    data = warning_number()
    return_data = {'data': data, 'comment': '未读异常次数', 'code': 1}
    des_data = des_en(return_data)
    return des_data


@router.get('/query_date', name='日期查询报警信息')
def get_warning_date(page, size, item):
    """
        日期查询报警信息
        ---
        # 参数信息
        |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
        |       ---- | ---- | ---- | ---- | ---- |
        |   page     | int | 页码 | 是 | |
        |   size     | int | 展示数量 | 是 | |
        |   item     | json | 时间类 | 是 | 包含一下数据|
        |   start_date  | date | 开始时间 | 是 | |
        |   end_date  | date | 结束时间 | 是 | |
    """
    page, size, item = int(des_de(page)), int(des_de(size)), des_de(item)
    item = ast.literal_eval(item)
    for key, value in item.items():
        item[key] = string_to_date(value)
    data = warning_date(page, size, item)
    return_data = {'data': data, 'comment': '日期获取报警信息', 'code': 1}
    des_data = des_en(return_data)
    return des_data


@router.get('/get_limit', name='获取上下限数据')
def get_limit_setting():
    """
           获取上下限数据
           ---
           # 参数信息
           |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
    """
    data = get_limit()
    return_data = {'data': data, 'comment': '获取上下限数据', 'code': 1}
    des_data = des_en(return_data)
    return des_data


@router.get('/limit_setting', name='上下限设置数据')
def update_limit_setting(item):
    """
        上下限设置数据
        ---
        # 参数信息
        |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
        |       ---- | ---- | ---- | ---- | ---- |
        |   item     | json | 时间类 | 是 | 包含一下数据|
        |   maximum  | int | 上限 | 是 | |
        |   minimum  | int | 下限 | 是 | |
    """
    item = des_de(item)
    item = ast.literal_eval(item)
    for key, value in item.items():
        item[key] = int(value)
    try:
        update_limit(item)
        return_data = {'data': '设置成功', 'comment': '上下限设置数据', 'code': 1}
        des_data = des_en(return_data)
    except:
        return_data = {'data': '设置失败', 'comment': '上下限设置数据', 'code': 0}
        des_data = des_en(return_data)
    return des_data


@router.get('/update_unread', name='修改未读信息')
def update_unread_data(data_id):
    """
        上下限设置数据
        ---
        # 参数信息
        |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
        |       ---- | ---- | ---- | ---- | ---- |
        |   data_id  | int | 数据id | 是 | |
    """
    data_id = int(des_de(data_id))
    try:
        update_unread(data_id)
        return_data = {'data': '设置成功', 'comment': '修改未读信息', 'code': 1}
        des_data = des_en(return_data)
    except:
        return_data = {'data': '设置失败', 'comment': '修改未读信息', 'code': 0}
        des_data = des_en(return_data)
    return des_data

