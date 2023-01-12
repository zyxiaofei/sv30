import time
from queue import Queue
import cv2
from pathlib import Path
from datetime import datetime
from domain.entity.video_camera import camera
from domain.service.hardware_control import get_plc_input_status, get_plc_input_register
from domain.repository.redis_connection import redis_control, set_redis, get_redis, exists_redis
from infrastructure.common.sludge_height import MeasurementThread
from domain.repository.database_connection import add_database, query_database
from infrastructure.common.models import MeasureDataFormation, WarningSign
from infrastructure.common.string_date_change import string_to_date
import asyncio


class video_and_record:
    instance = None

    def __new__(cls, *args, **kwargs):
        # 1.判断类属性是否为空对象，若为空说明第一个对象还没被创建
        if cls.instance is None:
            # 2.对第一个对象没有被创建，我们应该调用父类的方法，为第一个对象分配空间
            cls.instance = super().__new__(cls)
        # 3.把类属性中保存的对象引用返回给python的解释器
        return cls.instance

    def __init__(self):
        self.video_queue = Queue()
        self.suppress_time = []
        self.measurement = MeasurementThread()

    async def streaming(self, type_run=0):
        time.sleep(3)  # Because the modification time of plc may be delayed, it sleeps for 3s and waits for modification of other schemes.
        global cap
        cap_err = 0
        print('streaming', datetime.now())
        finish_time = get_plc_input_register('sedimentation_time_setting')
        print('finish_time', finish_time)
        cap = camera()
        print('摄像头开启', datetime.now())
        while True:
            success, frame = cap.read()
            await asyncio.sleep(0.1)
            if success:
                font = cv2.FONT_HERSHEY_SIMPLEX
                frame_date = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                frame = cv2.putText(frame, frame_date, (450, 20), font, 0.5, (0, 25, 25), 2, cv2.LINE_4)
                if type_run == 1 and int(get_plc_input_status(
                        'measuring_cylinder_high_water_mark')) == 1 and not self.measurement.show_sludge_height(
                        frame) == 0:
                    if int(get_redis('start_task')) == 0:
                        start_time = datetime.now()
                        set_redis("start_task", 1)
                        set_redis('start_record_time', start_time.strftime('%Y-%m-%d %H:%M:%S'))
                    else:
                        start_time = get_redis('start_record_time')
                        start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                        time_difference = (datetime.now() - start_time).seconds
                        if time_difference == finish_time:
                            print('finish_time', finish_time)
                            if time_difference not in self.suppress_time:
                                self.suppress_time.append(time_difference)
                                self.video_queue.put_nowait([time_difference, frame])
                            print(datetime.now())
                            print(start_time)
                            set_redis('end_record_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                            set_redis('measure_duration', finish_time / 60)
                            cap.release()
                            set_redis('state', 1)
                            print("over")
                            break
                        if time_difference not in self.suppress_time:
                            self.suppress_time.append(time_difference)
                            self.video_queue.put_nowait([time_difference, frame])
                ret, frame = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                       bytearray(frame) + b'\r\n')
            else:
                cap.release()
                cap = camera()
                cap_err += 1
                print('摄像头未正常打开!.', cap_err)
                if cap_err > 3:
                    err = {'msg': '摄像头未正常打开，请联系技术人员排查.'}
                    err = err.__str__()
                    redis_control(key="error_massage", value=err)
                    break

    def video_record(self, path, path_list):
        file_name = Path(path, './record_video.mp4')
        FILENAME = file_name.__str__()
        videoWriter = cv2.VideoWriter(FILENAME, cv2.VideoWriter_fourcc(*'avc1'), 1, (640, 480))
        data_list = {}
        return_data = {}
        records_time = []
        first_high = 0
        image = None

        while True:
            if self.video_queue.qsize() > 0:
                video_data = self.video_queue.get()
                videoWriter.write(video_data[1])
                image = video_data[1]
                if video_data[0] not in records_time:
                    if video_data[0] < 30:
                        measurement_data = self.measurement.show_sludge_height(video_data[1])
                        if measurement_data > first_high:
                            first_high = measurement_data
                            print(first_high)
                    elif (video_data[0] <= 600 and video_data[0] % 30 == 0) or \
                            (video_data[0] <= 1800 and video_data[0] % 60 == 0) or \
                            (video_data[0] > 1800 and video_data[0] % 300 == 0):
                        records_time.append(video_data[0])
                        measurement_data = self.measurement.show_sludge_height(video_data[1])
                        print('mea', video_data[0], measurement_data)
                        images_path = '../image/{path}.jpg'.format(path=video_data[0])
                        cv2.imwrite(images_path, video_data[1])
                        print('1st', first_high)
                        output_data = round(measurement_data / first_high * 100, 2)
                        if output_data > 100:
                            output_data = 100
                        data_list[video_data[0]] = output_data
                        return_data['measurement_data'] = str(data_list)

                        return_data['start_time'] = str(get_redis('start_record_time'))
                        redis_control(key="measurement_data", value=str(return_data))
            elif int(get_redis('state')) == 1:
                videoWriter.release()
                set_redis('state', 0)
                image_path = Path(path, './last.jpg')
                ImageName = image_path.__str__()
                cv2.imwrite(ImageName, image)
                start_time = get_redis('start_record_time')
                start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                end_time = get_redis('end_record_time')
                end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                measure_duration = int(float(get_redis('measure_duration')))
                last_time = measure_duration * 60
                last_current_measure_data = data_list[last_time]
                date = string_to_date(path_list[0])
                limit = query_database(cls_name=WarningSign)[0]
                max_limit = limit.maximum
                min_limit = limit.minimum
                if min_limit < last_current_measure_data < max_limit or not measure_duration == 30:
                    warning_sign = 1  # 0 异常 1 正常
                    read_sign = 1  # 0 未读 1 已读
                else:
                    warning_sign = 0
                    read_sign = 0
                type_run = int(get_redis('type_run'))
                add_database([MeasureDataFormation(measure_times=path_list[1],
                                                   current_measure_data=data_list,
                                                   last_current_measure_data=last_current_measure_data,
                                                   measure_date=date,
                                                   measure_duration=measure_duration,
                                                   measure_start_time=start_time,
                                                   measure_end_time=end_time,
                                                   measure_type=type_run,
                                                   warning_sign=warning_sign,
                                                   read_sign=read_sign
                                                   )])
                break
            elif int(get_plc_input_register('program_flag')) == 1:
                print('压制视频强制终止')
                break
