from domain.repository.database_connection import query_database
from infrastructure.common.models import TimerSetting
from domain.repository.database_connection import add_database, delete_database
from infrastructure.common.timer import remove_scheduler, add_scheduler
from infrastructure.common.automatic_task import send_task_run_time


def get_timer_setting():
    data = query_database(cls_name=TimerSetting, type_data=0, filter_data={TimerSetting.enable_type == 1})
    return_data = {}
    if data:
        return_data['type'] = 1
        return_data['data'] = []
        for item in data:
            return_data['sedimentation_time'] = item.sedimentation_time
            return_data['data'].append({'beginning_time': item.beginning_time,
                                        'ending_time': item.ending_time})
    else:
        return_data['type'] = 0
        return return_data

    return return_data


def update_timer_setting(item):
    err_code = item['err_code']
    if err_code == 0:
        return_data = '不允许出现交叉时间,请调整后重试'
        return return_data, err_code
    elif err_code == 1:
        sys_data = query_database(cls_name=TimerSetting, type_data=0)
        for system_data in sys_data:
            remove_scheduler(job_id=system_data.uuid)
        if item['data_type'] == 0:
            delete_database(cls_name=TimerSetting)
            add_database(
                [TimerSetting(sedimentation_time=30, beginning_time='09:00', ending_time='10:30', enable_type=0),
                 TimerSetting(sedimentation_time=30, beginning_time='16:00', ending_time='17:30', enable_type=0)])
        elif item['data_type'] == 1:

            delete_database(cls_name=TimerSetting)
            sedimentation = item['sedimentation_time']
            date_time = item['time_data']
            data_list = []
            for data in date_time:
                data_list.append(TimerSetting(sedimentation_time=sedimentation, beginning_time=data[0],
                                              ending_time=data[1], enable_type=1))
            add_database(data_list)

        timer_data = query_database(cls_name=TimerSetting, type_data=0)
        for scheduler in timer_data:

            date_time = scheduler.beginning_time.split(':')
            add_scheduler(task=send_task_run_time, job_id=scheduler.uuid, hour=int(date_time[0]),
                          minute=int(date_time[1]))
        return_data = '修改成功'
        return return_data, err_code
