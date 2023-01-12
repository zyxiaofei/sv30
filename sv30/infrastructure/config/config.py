import configparser
import os


class Config(object):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        pass

    def get_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8")
        return config

    def get_database_name(self):
        config = self.get_config(os.path.join(Config.BASE_DIR, 'config.ini'))
        return dict(config.items("database_name"))

    def get_des_key(self):
        config = self.get_config(os.path.join(Config.BASE_DIR, 'config.ini'))
        return dict(config.items("des_key"))

    def get_plc_coil_read_only(self):
        config = self.get_config(os.path.join(Config.BASE_DIR, 'config.ini'))
        return dict(config.items("plc_coil_read_only")+config.items("plc_coil_read_and_write"))

    def get_plc_coil_read_and_write(self):
        config = self.get_config(os.path.join(Config.BASE_DIR, 'config.ini'))
        return dict(config.items("plc_coil_read_and_write"))

    def get_plc_input_status_read_only(self):
        config = self.get_config(os.path.join(Config.BASE_DIR, 'config.ini'))
        return dict(config.items("plc_input_status_read_only"))

    def get_plc_input_register_read_only(self):
        config = self.get_config(os.path.join(Config.BASE_DIR, 'config.ini'))
        return dict(config.items("plc_input_register_read_only")+config.items("plc_input_register_read_and_write"))

    def get_plc_input_register_read_and_write(self):
        config = self.get_config(os.path.join(Config.BASE_DIR, 'config.ini'))
        return dict(config.items("plc_input_register_read_and_write"))

