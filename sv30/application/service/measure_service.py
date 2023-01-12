from domain.repository.database_connection import query_database
from infrastructure.common.models import MeasureDataFormation
from infrastructure.common.string_date_change import string_to_date


def get_measure_list(year: str = None, month: str = None, day: str = None):
    video_date = year + "-" + month + "-" + day
    date = string_to_date(video_date)
    return_data = []
    base_data = query_database(cls_name=MeasureDataFormation,
                               type_data=0,
                               filter_data={MeasureDataFormation.measure_date == date})
    for data in base_data:
        return_data.append(
            {"id": data.id,
             "measure_times": data.measure_times,
             "start_time": str(data.measure_start_time),
             "end_time": str(data.measure_end_time),
             "measure_duration": data.measure_duration,
             "measure_type": data.measure_type})
    return return_data


def measure_data(measure_id):
    data = query_database(cls_name=MeasureDataFormation,
                          type_data=1,
                          filter_data={MeasureDataFormation.id == measure_id})
    return_data = {'data': data.current_measure_data,
                   "start_time": str(data.measure_start_time),
                   "measure_duration": data.measure_duration}
    return return_data


def get_history_data_list(start_time, end_time):
    # start_date = string_to_date(start_time)
    # end_date = string_to_date(end_time)
    start_date = start_time
    end_date = end_time
    return_data = []
    base_data = query_database(cls_name=MeasureDataFormation,
                               type_data=0,
                               filter_data={MeasureDataFormation.measure_date >= start_date,
                                            MeasureDataFormation.measure_date <= end_date})

    for data in base_data:
        return_data.append(
            {"id": data.id,
             "measure_times": data.measure_times,
             "start_time": str(data.measure_start_time),
             "end_time": str(data.measure_end_time),
             "last_current_measure_data": data.last_current_measure_data,
             "measure_duration": data.measure_duration,
             "measure_type": data.measure_type})
    return return_data
