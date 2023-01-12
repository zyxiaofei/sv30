# -*- encoding: utf-8 -*-

# from pytz import timezone

# timezone = 'Asia/Shanghai'

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from infrastructure.config.config import Config


config = Config()
database_name = config.get_database_name().get("database_name")
scheduler = AsyncIOScheduler()


def start_apscheduler():
    '''初始化内容'''
    executors = {
        'default': {'type': 'threadpool', 'max_workers': 10},  # 最大工作线程数10
        'processpool': ProcessPoolExecutor(max_workers=4)  # 最大工作进程数为4
    }
    job_defaults = {
        'coalesce': False,  # 关闭新job的合并，当job延误或者异常原因未执行时
        'max_instances': 4,  # 并发运行新job默认最大实例多少
        'misfire_grace_time': 100
    }
    # .. do something else here, maybe add jobs etc.

    scheduler.configure(executors=executors, job_defaults=job_defaults,
                        timezone='Asia/Shanghai')  # 上海时间作为调度程序的时区
    scheduler.start()


def remove_scheduler(job_id):
    try:
        scheduler.remove_job(job_id=job_id)
    except:
        pass


def add_scheduler(task, job_id, hour: int, minute: int):
    try:
        scheduler.add_job(task, 'cron', hour=hour, minute=minute, id=job_id)
    except:
        print("定时器错误")

