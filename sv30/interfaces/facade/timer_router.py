import ast
from fastapi import APIRouter
from application.service.timer_service import get_timer_setting, update_timer_setting
from interfaces.assembler.data_decide import timer_parameter_decide
from interfaces.assembler.des import des_en, des_de

router = APIRouter()


@router.get('/timer_setting', name='获取定时器设置')
def get_settlement_setting():
    """
        获取定时器设置
        ---
        # 参数信息
        |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
        |       ---- | ---- | ---- | ---- | ---- |

    """
    data = get_timer_setting()
    return_data = {'data': data, 'comment': '定时器设置', 'code': 1}
    des_data = des_en(return_data)
    return des_data


@router.get('/set_timer_setting', name='修改定时器设置数据')
def update_settlement_setting(item: str):
    """
        修改定时器设置数据
        ---
        # 参数信息
        |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
        |       ---- | ---- | ---- | ---- | ---- |
        |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
        | ---- | ---- | ---- | ---- | ---- |
        | item | str | 加密数据类 | 是 | 一个加密json类 |
        | data_type | int | 启用类型 | 是 | 0:系统 1:自定义 |
        | sedimentation_time | int | 沉降时间 | 是 | 30|
        | time_data | list | 时间列表 | 是 |包含一下数据[[start_time,end_time]] |
        | start_time | string | 开始时间 | 是 | 00:00|
        | end_time | string | 结束时间 | 是 | 00:00|
    """

    item = des_de(item)
    item = ast.literal_eval(item)
    decide_data = timer_parameter_decide(item)
    data, code = update_timer_setting(decide_data)
    return_data = {'data': data, 'comment': '定时器设置数据', 'code': code}
    des_data = des_en(return_data)
    return des_data

