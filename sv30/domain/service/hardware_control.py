from domain.entity.hardware_entity import hardware_entity

plc = hardware_entity()


def get_plc_coils(function_name):
    return plc.query_hardware_coil(function_name)


def set_plc_coils(function_name):
    plc.send_command_coil(function_name)


def get_plc_input_status(function_name):
    return plc.query_hardware_input_status(function_name)


def get_plc_input_register(function_name):
    return plc.query_hardware_input_register(function_name)


def set_plc_input_register(function_name, send_data):
    plc.send_command_input_register(function_name, send_data)
