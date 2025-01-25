import configparser
import os


def load_config():
    config_1 = configparser.ConfigParser()
    config_file_path = os.path.join(os.path.dirname(__file__), '../config.ini')
    config_1.read(config_file_path)
    return config_1


config = load_config()
