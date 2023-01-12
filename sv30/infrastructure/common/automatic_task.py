from domain.repository.redis_connection import redis_control


def send_task_run_time():
    """发送自动运行指令"""
    redis_control(key="automatic_task", value=1)

