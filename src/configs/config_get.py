import configparser
import os
from pathlib import Path


def load_ini_config():
    config_parser = configparser.ConfigParser()
    config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')

    # 指定使用UTF-8编码读取配置文件
    with open(config_file_path, 'r', encoding='utf-8-sig') as f:
        config_parser.read_file(f)
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
        'zhipu_api_key': ini_config.get('API_KEYS', 'zhipu_api_key', fallback=''),
        'deepseek_api_key': ini_config.get('API_KEYS', 'deepseek_api_key', fallback=''),
        'moonshot_api_key': ini_config.get('API_KEYS', 'moonshot_api_key', fallback=''),
    }


def get_ppt_xh_config(ini_config):
    """从ini配置中加载PPT讯飞配置"""
    return {
        'APPId': ini_config.get('PPT_XH', 'APPId'),
        'APISecret': ini_config.get('PPT_XH', 'APISecret')
    }


# 加载ini配置
ini_con = load_ini_config()

# 完整配置字典
config = {
    'api_keys': get_api_keys_config(ini_con),
    'database': get_database_config(ini_con),
    'ppt_xh': get_ppt_xh_config(ini_con)
}
