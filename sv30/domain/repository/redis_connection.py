from infrastructure.dao.redis_setting import redis_conn


def redis_control(key, value):
    redis_conn.rpush(key, value)


def get_redis(key):
    return redis_conn.get(key)


def set_redis(key, value):
    redis_conn.set(key, value)


def exists_redis(key):
    return redis_conn.exists(key)


def delete_redis(key):
    return redis_conn.delete(key)


def clear_redis():
    redis_conn.flushdb()
