from application.service.measure_service import measure_data, get_measure_list, get_history_data_list
from application.service.sv30_service import start_task, hardware_current_status, system_demonstration, \
    next_settling_time, end_task
from fastapi import APIRouter
from interfaces.assembler.des import des_en, des_de
from interfaces.assembler.str_to_data import string_to_date

router = APIRouter()


@router.get('/get_file/list', name='获取文件列表')
def get_video_path_list(year: str = None, month: str = None, day: str = None):
    """
        获取文件列表
        ---
        # 参数信息
        |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
        |       ---- | ---- | ---- | ---- | ---- |
        |   year     | string | 年 | 是 | |
        |    month   | string | 月 | 是 | |
        |    day    | string | 日 | 是 | |
    """
    year, month, day = des_de(year), des_de(month), des_de(day)
    data = get_measure_list(year, month, day)
    return_data = {'data': data, 'comment': '文件列表', 'code': 1}
    des_data = des_en(return_data)
    return des_data


@router.get("/get_file", name='获取沉淀数据')
def get_measure_data(measure_id):
    """
        获取沉淀数据
        ---
        # 参数信息
        |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
        |       ---- | ---- | ---- | ---- | ---- |
        |   measure_id     | int | 沉淀数据id | 是 | |
    """
    measure_id = int(des_de(measure_id))
    data = measure_data(measure_id)
    return_data = {'data': data, 'comment': '沉淀数据', 'code': 1}
    des_data = des_en(return_data)
    return des_data


@router.get("/start_task", name='开始任务')
def start(type_run, run_time):
    """
        开始任务
        ---
        # 参数信息
        |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
        |       ---- | ---- | ---- | ---- | ---- |
        |   type_run   | int | 任务类型 | 是 | 0 自动 1 手动|
        |   run_time   | int | 沉淀时间 | 是 | 单位分钟 |
    """
    type_run = int(des_de(type_run))
    run_time = int(des_de(run_time))
    start_task(type_run, run_time)
    return


@router.get("/end_task", name='结束任务')
def end():
    """
        结束任务
        ---
        # 参数信息
        |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
        |       ---- | ---- | ---- | ---- | ---- |
    """
    end_task()
    return


@router.get("/system_demonstration", name='系统演示')
def start_demonstration():
    """
        系统演示
        ---
        # 参数信息
        |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
        |       ---- | ---- | ---- | ---- | ---- |

    """
    system_demonstration()
    return


@router.get("/current_status", name='获取当前设备状态')
def hardware_current():
    """
        获取当前设备状态
        ---
        # 参数信息
        |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
        |       ---- | ---- | ---- | ---- | ---- |

    """
    status_code = hardware_current_status()
    return_data = {'data': status_code, 'comment': '当前设备状态', 'code': 1}
    des_data = des_en(return_data)
    return des_data


@router.get('/get_history_file', name='获取历史沉淀数据')
def get_history_data(start_date, end_date):
    """
        获取历史沉淀数据
        ---
        # 参数信息
        |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
        |       ---- | ---- | ---- | ---- | ---- |
        |   start_date     | date | 年 | 是 | |
        |    end_date   | date | 月 | 是 | |

    """
    start_date, end_date = des_de(start_date), des_de(end_date)
    start_date, end_date = string_to_date(start_date), string_to_date(end_date)
    data = get_history_data_list(start_time=start_date, end_time=end_date)
    return_data = {'data': data, 'comment': '历史沉淀数据', 'code': 1}
    des_data = des_en(return_data)
    return des_data


@router.get('/get_next_time', name='获取下次沉淀时间')
def get_next_settling_time():
    """
        获取下次沉淀时间
        ---
        # 参数信息
        |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
        |       ---- | ---- | ---- | ---- | ---- |

    """
    data = next_settling_time()
    return_data = {'data': data, 'comment': '下次沉淀数据', 'code': 1}
    des_data = des_en(return_data)
    return des_data
