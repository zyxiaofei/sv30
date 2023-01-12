import math
from domain.repository.database_connection import add_database, query_database, delete_database, update_database
from infrastructure.common.models import WarningSign, MeasureDataFormation


def warning_date(page, size, item):
    start_date = item['start_date']
    end_date = item['end_date']
    base_data = query_database(cls_name=MeasureDataFormation, type_data=0,
                               filter_data={MeasureDataFormation.measure_date >= start_date,
                                            MeasureDataFormation.measure_date <= end_date,
                                            MeasureDataFormation.warning_sign == 0})
    if base_data:
        data_list = []
        for data in base_data:
            data_list.append({'measure_start_time': str(data.measure_start_time),
                              'last_current_measure_data': data.last_current_measure_data,
                              'read_sign': data.read_sign})
        data_list = list(reversed(data_list))
        page_size = len(base_data)
        return_data = {'data': data_list[(size * (page - 1)):(size * page)], 'page': page,
                       'page_size': page_size}
        return return_data
    else:
        return_data = {'data': [], 'page': 1,
                       'page_size': 1}
        return return_data


def warning_message(page, size):
    base_data = query_database(cls_name=MeasureDataFormation, type_data=0,
                               filter_data={MeasureDataFormation.warning_sign == 0,
                                            MeasureDataFormation.read_sign == 0})
    data_list = []
    for data in base_data:
        data_list.append({'id': data.id,
                          'measure_start_time': str(data.measure_start_time),
                          'last_current_measure_data': data.last_current_measure_data,
                          'read_sign': data.read_sign})
    page_size = len(base_data)
    data_list = list(reversed(data_list))
    return_data = {'data': data_list[(size * (page - 1)):(size * page)], 'page': page,
                   'page_size': page_size}
    return return_data


def warning_number():
    base_data = query_database(cls_name=MeasureDataFormation, type_data=0,
                               filter_data={MeasureDataFormation.warning_sign == 0,
                                            MeasureDataFormation.read_sign == 0})
    return_data = base_data.__len__()
    return return_data


def get_limit():
    base_data = query_database(cls_name=WarningSign, type_data=0, filter_data={})
    base_data = base_data[0]
    return_data = {'maximum': base_data.maximum, 'minimum': base_data.minimum}
    return return_data


def update_limit(item):
    maximum = item['maximum']
    minimum = item['minimum']
    delete_database(cls_name=WarningSign)
    add_database([WarningSign(maximum=maximum, minimum=minimum)])


def update_unread(data_id):
    update_data = {'read_sign': 1}
    update_database(cls_name=MeasureDataFormation, update_data=update_data,
                    filter_data={MeasureDataFormation.id == data_id})
