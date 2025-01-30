import configparser
import os


def load_ini_config():
    config_parser = configparser.ConfigParser()
    config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config_parser.read(config_file_path)
    return config_parser


def get_database_config(ini_config):
    """从ini配置中加载数据库配置"""
    return {
        'host': ini_config.get('DATABASE', 'host'),
        'port': ini_config.getint('DATABASE', 'port'),
        'user': ini_config.get('DATABASE', 'user'),
        'password': ini_config.get('DATABASE', 'password'),
        'database': ini_config.get('DATABASE', 'database')
    }


def get_api_keys_config(ini_config):
    """从ini配置中加载API密钥配置"""
    return {
        'tongyi_api_key': ini_config.get('API_KEYS', 'tongyi_api_key', fallback=''),
        'zhipu_api_key': ini_config.get('API_KEYS', 'zhipu_api_key', fallback='')
    }


# 加载ini配置
ini_config = load_ini_config()

# 完整配置字典
config = {
    'api_keys': get_api_keys_config(ini_config),
    'database': get_database_config(ini_config)
}
