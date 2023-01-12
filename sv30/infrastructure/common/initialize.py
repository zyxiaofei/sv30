from sqlalchemy import create_engine
import os
import threading

from domain.repository.redis_connection import redis_control, clear_redis
from infrastructure.config.config import Config
from domain.service.control_plc_status_code import set_status_code
from domain.service.hardware_control import get_plc_input_register, set_plc_coils
from infrastructure.common.timer import start_apscheduler, add_scheduler
from domain.repository.database_connection import query_database, add_database
from infrastructure.common.models import TimerSetting, WarningSign
from infrastructure.common.automatic_task import send_task_run_time

config = Config()


def initialize_database():
    database_name = config.get_database_name().get("database_name")
    if not os.path.exists("{database_name}".format(database_name=database_name)):
        engine = create_engine(
            'sqlite:///{database_name}'.format(database_name=database_name), connect_args={"check_same_thread": False},
            encoding='utf8', echo=False, echo_pool=False,
            pool_recycle=3600, pool_pre_ping=True)
        from infrastructure.common.models import Base
        Base.metadata.create_all(engine)
    else:
        pass


def initialize_internal_storage():
    try:
        clear_redis()
    except:
        print('初始化删除redis的keys错误')


def real_time_status_code():
    value = get_plc_input_register('program_flag')
    set_status_code(value=value)
    initialize_status_code()


def initialize_status_code():
    threading.Timer(1, real_time_status_code).start()


def initialize_timer():
    start_apscheduler()
    timer_data = query_database(cls_name=TimerSetting, type_data=0)
    if not timer_data:
        add_database([TimerSetting(sedimentation_time=30, beginning_time='09:00', ending_time='10:30', enable_type=0),
                      TimerSetting(sedimentation_time=30, beginning_time='16:00', ending_time='17:30', enable_type=0)])
        timer_data = query_database(cls_name=TimerSetting, type_data=0)
    for scheduler in timer_data:
        date_time = scheduler.beginning_time.split(':')
        add_scheduler(task=send_task_run_time, job_id=scheduler.uuid, hour=int(date_time[0]),
                      minute=int(date_time[1]))


def initialize_limit():
    limit = query_database(cls_name=WarningSign, type_data=0)
    if not limit:
        add_database([WarningSign(minimum=20, maximum=50)])


def plc_program_startup_inspection():
    if int(get_plc_input_register('program_flag')) == 3:
        set_plc_coils("end_operation_immediately_and_start")
        set_plc_coils("the_reset_operation_starts")
        err = {'msg': '程序异常，终止沉降.', 'status_code': 0}
        err = err.__str__()
        redis_control(key="error_massage", value=err)