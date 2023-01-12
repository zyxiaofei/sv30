from domain.repository.redis_connection import redis_control


class status_code(object):
    def __init__(self):
        self._code = None

    def _set_value(self, value):
        if self._code == value:
            return self._code
        redis_control(key="status_code", value=value)
        return value

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = self._set_value(value)
