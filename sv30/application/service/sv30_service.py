import datetime

from domain.service.control_plc_status_code import get_status_code
from domain.service.hardware_control import set_plc_coils, get_plc_input_register, set_plc_input_register
from domain.service.streaming_and_record import video_and_record
from domain.repository.database_connection import query_database
from domain.repository.redis_connection import set_redis, redis_control
from infrastructure.common.record_path import record_video_path
from infrastructure.common.models import TimerSetting
import threading


def record():
    path, path_list = record_video_path()
    record_task = threading.Thread(target=video.video_record, name='record', args=(path, path_list))
    print('线程状态1:', record_task.is_alive())
    print('线程池1', threading.enumerate())
    record_task.start()

    print('线程状态2:', record_task.is_alive())
    print('线程池2', threading.enumerate())


def hardware_current_status():
    return get_status_code()


def start_task(type_run, run_time):
    global video
    video = video_and_record()
    if int(get_plc_input_register('program_flag')) == 1:
        run_time = run_time * 60
        set_plc_input_register('sedimentation_time_setting', run_time)
        set_redis('state', 0)
        set_redis("start_task", 0)
        set_plc_coils("completion_of_external_signal_given")
        set_plc_coils("immediately_start_the_measurement_operation")
        print('plc_time', datetime.datetime.now())
        set_redis('type_run', type_run)
        record()
    else:
        err = {'msg': '设备已经运行.', 'status_code': 0}
        err = err.__str__()
        redis_control(key="error_massage", value=err)


def end_task():
    if int(get_plc_input_register('program_flag')) == 1:
        err = {'msg': '设备没有运行.', 'status_code': 0}
        err = err.__str__()
        redis_control(key="error_massage", value=err)
    else:
        set_plc_coils("end_operation_immediately_and_start")
        set_plc_coils("the_reset_operation_starts")



def system_demonstration():
    if int(get_plc_input_register('program_flag')) == 1:
        set_plc_coils("start_the_demonstration_operation")
    else:
        err = {'msg': '设备已经运行.', 'status_code': 0}
        err = err.__str__()
        redis_control(key="error_massage", value=err)


def next_settling_time():
    time_list = []
    data_list = query_database(cls_name=TimerSetting, type_data=0)
    for data in data_list:
        data_time = data.beginning_time.split(':')
        settling_time_hour = int(data_time[0])
        settling_time_minute = int(data_time[1])
        settling_time = settling_time_hour * 3600 + settling_time_minute * 60
        time_list.append(settling_time)
    time_list.sort()
    now_time = datetime.datetime.now().hour * 3600 + datetime.datetime.now().minute * 60
    qualified_time = [time for time in time_list if time > now_time]
    if qualified_time:
        min_time = min(qualified_time)
        hour = int(min_time / 3600).__str__().zfill(2)
        minute = int(min_time % 3600 / 60).__str__().zfill(2)
        date = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d') + ' {}:{}:{}'.format(hour,
                                                                                                              minute,
                                                                                                              '00')
    else:
        min_time = min(time_list)
        hour = int(min_time / 3600).__str__().zfill(2)
        minute = int(min_time % 3600 / 60).__str__().zfill(2)
        date = (datetime.date.today()).strftime('%Y-%m-%d') + ' {}:{}:{}'.format(hour, minute, '00')
    return date
