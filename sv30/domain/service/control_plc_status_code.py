from domain.entity.plc_status_code import status_code

code = status_code()


def get_status_code():
    return code.code


def set_status_code(value):
    code.code = value
