# -*- coding=utf-8
import os
import platform
from enum import Enum

import pkg_resources

from common.base import meta_singeton as meta_singeton_base
PROD = 'prod'
TEST = 'test'
DEV = 'dev'
ENV_LIST = [PROD, TEST, DEV]
APP_ENV = 'APP_ENV'
DEBUG = 'DEBUG'

ROLE = 'ROLE'
MASTER = 'master'  # 是否是master node


class PlatformEnum(Enum):
    MACOS = 'Darwin'
    WINDOWS = 'Windows'
    LINUX = 'Linux'


IS_MACOS = platform.system() == PlatformEnum.MACOS.value
IS_WINDOWS = platform.system() == PlatformEnum.WINDOWS.value
IS_LINUX = platform.system() == PlatformEnum.LINUX.value

# 跟目录
ROOT_DIR = pkg_resources.resource_filename('common.logger', '') + '/../'


class Instance(metaclass=meta_singeton_base.MetaSingleton):
    # dev-开发｜test-测试｜prod-生产
    app_env: str
    # 是否debug模式
    debug: bool
    # master - master node | 其他node
    node_role: str
    
    def __init__(self):
        app_env = os.environ.get(APP_ENV)
        if app_env not in ENV_LIST:
            raise ValueError(f"app_env 配置错误！！！curr env:{app_env}")
        self.app_env = app_env
        self.debug = os.environ.get(DEBUG, False)
        self.node_role = os.environ.get(ROLE, None)
        
        print(f'=> node config: 环境-{self.app_env}；debug：{self.debug}; node-role：{self.node_role}')
    
    def is_prod(self):
        return self.app_env == PROD
    
    def is_test(self):
        return self.app_env == TEST
    
    def is_dev(self):
        return self.app_env == DEV
    
    def get_env(self):
        return self.app_env
    
    def is_debug(self):
        return self.debug
    
    def is_master(self):
        return self.node_role == MASTER
    
    def get_env_config_file(self):
        return f'{ROOT_DIR}/config/{self.app_env}.yml'
    
    def get_application_common_file(self):
        return f'{ROOT_DIR}/config/application.yml'


# 获取根目录的文件夹
def get_root_dir() -> str:
    return ROOT_DIR
