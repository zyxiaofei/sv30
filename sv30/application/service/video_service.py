from domain.service.streaming_and_record import video_and_record
from infrastructure.common.record_path import get_video_dir
from pathlib import Path
import os


def live_streaming(type_run):
    video = video_and_record()
    return_data = video.streaming(type_run=int(type_run))
    return return_data


def get_file_path(file_type: str = None, year: str = None, month: str = None, day: str = None, num: str = '1'):
    dir_name = get_video_dir()
    files = None
    if file_type == 'video':
        files = Path(dir_name, f'{year}/{month}/{day}/{num}/record_video.mp4')
    elif file_type == 'image':
        files = Path(dir_name, f'{year}/{month}/{day}/{num}/last.jpg')
    if not os.path.exists(files):
        return_data = {'data': '文件不存在！', 'comment': '视频与图像文件', 'code': 0}
        return return_data
    return files
