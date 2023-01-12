from domain.repository.redis_connection import redis_control
from modbus_tk import modbus_tcp
import time


def hardware_connect(times=0):
    try:
        hardware_address = '192.168.2.1'
        port = 2000
        master = modbus_tcp.TcpMaster(hardware_address, port)
        master.set_timeout(60)
        master.set_verbose(True)
        return master
    except:
        times += 1
        if times > 3:
            return_data = {'status_code': 0, 'msg': '设备链接超时，请联系技术人员排查.'}
            return_data = return_data.__str__()
            redis_control(key='error_massage', value=return_data)
            return return_data
        time.sleep(2)
        hardware_connect(times)
