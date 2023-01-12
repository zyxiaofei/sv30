from infrastructure.config.config import Config
from domain.repository.redis_connection import redis_control
from infrastructure.utils.hardware_helper import hardware_connect
import modbus_tk.defines as cst


class hardware_entity:
    def __init__(self):
        self.hardware = hardware_connect()
        self.config = Config()

    def query_hardware_coil(self, function_name):

        coil = self.config.get_plc_coil_read_only().get(function_name)
        if isinstance(self.hardware, dict):
            err = "plc连接异常"
            redis_control(key="error_massage", value=err)
            return 0
        try:
            ret = self.hardware.execute(1, cst.READ_COILS, int(coil), 1)
            return_data = ret[0]
            return return_data
        except:
            err = {'msg': '设备链接异常，请联系技术人员排查.', 'status_code': coil}
            err = err.__str__()
            redis_control(key="error_massage", value=err)
            return 0

    def send_command_coil(self, function_name):
        coil = self.config.get_plc_coil_read_and_write().get(function_name)
        if isinstance(self.hardware, dict):
            err = "plc连接异常"
            redis_control(key="error_massage", value=err)
            return 0
        try:
            self.hardware.execute(1, cst.WRITE_SINGLE_COIL, int(coil), output_value=0)
            self.hardware.execute(1, cst.WRITE_SINGLE_COIL, int(coil), output_value=1)
            print(coil, "ok")
        except:
            err = {'msg': '设备链接异常，请联系技术人员排查.', 'status_code': coil}
            err = err.__str__()
            redis_control(key="error_massage", value=err)
            return 0

    def query_hardware_input_status(self, function_name):
        input_status = self.config.get_plc_input_status_read_only().get(function_name)
        if isinstance(self.hardware, dict):
            err = "plc连接异常"
            redis_control(key="error_massage", value=err)
            return 0
        try:
            ret = self.hardware.execute(1, cst.READ_DISCRETE_INPUTS, int(input_status), 1)
            return_data = ret[0]
            return return_data
        except:
            err = {'msg': '设备链接异常，请联系技术人员排查.', 'status_code': input_status}
            err = err.__str__()
            redis_control(key="error_massage", value=err)
            return 0

    def query_hardware_input_register(self, function_name):
        input_register = self.config.get_plc_input_register_read_only().get(function_name)
        if isinstance(self.hardware, dict):
            err = "plc连接异常"
            redis_control(key="error_massage", value=err)
            return 0
        try:
            ret = self.hardware.execute(1, cst.READ_HOLDING_REGISTERS, int(input_register), 1)
            return_data = ret[0]
            return return_data
        except:
            err = {'msg': '设备链接异常，请联系技术人员排查.', 'status_code': input_register}
            err = err.__str__()
            redis_control(key="error_massage", value=err)
            return 0

    def send_command_input_register(self, function_name, send_data):
        input_register = self.config.get_plc_input_register_read_and_write().get(function_name)
        if isinstance(self.hardware, dict):
            err = "plc连接异常"
            redis_control(key="error_massage", value=err)
            return 0
        try:
            self.hardware.execute(1, cst.WRITE_SINGLE_REGISTER, int(input_register), output_value=send_data)
        except:
            err = {'msg': '设备链接异常，请联系技术人员排查.', 'status_code': input_register}
            err = err.__str__()
            redis_control(key="error_massage", value=err)
            return 0
