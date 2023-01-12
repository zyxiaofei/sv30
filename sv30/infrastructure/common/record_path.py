import os
from pathlib import Path
from datetime import datetime


def record_video_path():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    this_year = datetime.now().strftime('%Y')
    this_month = datetime.now().strftime('%m')
    this_day = datetime.now().strftime('%d')

    num = 1
    while True:
        this_file_dir_path = Path(base_dir, f'./record_video/{this_year}/{this_month}/{this_day}/{str(num)}/')
        if os.path.isdir(this_file_dir_path):
            num += 1
        else:
            os.makedirs(this_file_dir_path)
            break

    path_list = [this_year + "-" + this_month + "-" + this_day, num]
    return this_file_dir_path, path_list


def get_video_dir():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    video_path = Path(base_dir, f'./record_video/')
    return video_path
