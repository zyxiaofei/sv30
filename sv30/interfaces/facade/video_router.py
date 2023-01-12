from fastapi import APIRouter
from application.service.video_service import live_streaming, get_file_path
from fastapi.responses import StreamingResponse, FileResponse
import os

router = APIRouter()


@router.get("/live/{types}", name="推流任务")
def live(types):
    """
        推流任务
        ---
        # 参数信息
        |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
        |       ---- | ---- | ---- | ---- | ---- |
        |   types     | int | 任务类型 | 是 | 0 不录象 1 录像|
    """
    return StreamingResponse(live_streaming(type_run=int(types)),
                             media_type="multipart/x-mixed-replace;boundary=frame")


@router.get('/file/video/{year}/{month}/{day}/{num}', name='获取视频文件')
def get_video(year: str = None, month: str = None, day: str = None, num: str = '1'):
    """
        获取视频文件
        ---
        # 参数信息
        |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
        |       ---- | ---- | ---- | ---- | ---- |
        |   year     | string | 年 | 是 | |
        |   month     | string | 月 | 是 | |
        |   day     | string | 日 | 是 | |
        |   num     | string | 次数 | 是 | |

    """
    # year, month, day, num = des_de(year), des_de(month), des_de(day), int(des_de(num))

    return_data = get_file_path('video', year, month, day, num)
    video_size = os.path.getsize(return_data)
    return FileResponse(path=return_data, headers={'Content-Length': str(video_size), 'Content-Type': 'video/mp4',
                                                   'Content-Range': f'bytes 0-{str(video_size)}/{str(video_size)}',
                                                   'Accept-Ranges': 'bytes'
                                                   })


@router.get('/file/image/{year}/{month}/{day}/{num}', name='获取图像文件', response_class=FileResponse)
def get_image(year: str = None, month: str = None, day: str = None, num: str = '1'):
    """
        获取图像文件
        ---
        # 参数信息
        |  传入参数    |  类型 |  说明   |  是否必填    |   附加信息 |
        |       ---- | ---- | ---- | ---- | ---- |
        |   year     | string | 年 | 是 | |
        |   month     | string | 月 | 是 | |
        |   day     | string | 日 | 是 | |
        |   num     | string | 次数 | 是 | |

    """
    # year, month, day, num = des_de(year), des_de(month), des_de(day), int(des_de(num))

    return_data = get_file_path('image', year, month, day, num)
    return return_data
