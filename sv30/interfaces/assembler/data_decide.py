def timer_parameter_decide(item):
    data_type = item['data_type']
    begin_end_time = []
    if data_type == 0:
        item['err_code'] = 1
        return item
    else:
        for t in item['time_data']:
            start_date_time = t[0].split(':')
            start_date_hour = int(start_date_time[0])
            start_date_minute = int(start_date_time[1])
            start_time = start_date_hour * 3600 + start_date_minute * 60
            end_date_time = t[1].split(':')
            end_date_hour = int(end_date_time[0])
            end_date_minute = int(end_date_time[1])
            end_time = end_date_hour * 3600 + end_date_minute * 60
            begin_end_time.append((start_time, end_time))
        begin_end_time = sorted(begin_end_time, key=lambda tup: tup[0])
        '''
        时间重复判断
        '''

        for n in range(len(begin_end_time) - 1):
            if begin_end_time[n + 1][0] <= begin_end_time[n][0] <= begin_end_time[n + 1][1] or \
               begin_end_time[n + 1][0] <= begin_end_time[n][1] <= begin_end_time[n + 1][1]:
                item['err_code'] = 0
                return item
        item['err_code'] = 1
        return item
