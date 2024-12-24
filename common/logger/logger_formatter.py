import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import pytz
from dataclasses_json import dataclass_json, DataClassJsonMixin

from common.env import env
from common.utils.common import get_host_name

CATEGORY_DEFAULT = 'default'
CATEGORY_API_REQUEST = 'api-service-request'
CATEGORY_GLOBAL_INTERFACE_MONITOR = 'global_app_interface_monitor'


@dataclass_json()
@dataclass
class ApiRequest(DataClassJsonMixin):
    traceid: Optional[str] = None
    url: Optional[str] = None
    header: any = None
    body: Optional[str] = None
    method: Optional[str] = None
    result: Optional[str] = None
    result_status: Optional[int] = None
    cost_time: Optional[int] = None
    error: Optional[str] = None


class GlobalInterfaceMonitor(DataClassJsonMixin):
    result: Optional[str] = None
    result_status: Optional[int] = None
    cost_time: Optional[int] = None


LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


class LogFormatter(logging.Formatter):
    datefmt = LOG_DATE_FORMAT
    green = "\x1b[32;22m"
    yellow = "\x1b[33;1m"
    red = "\x1b[31;1m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    record = "{record}"
    FORMATS = {
        logging.DEBUG   : green + record + reset,
        logging.INFO    : green + record + reset,
        logging.WARNING : yellow + record + reset,
        logging.ERROR   : red + record + reset,
        logging.CRITICAL: bold_red + record + reset
    }
    
    def format_with_color(self, level, mesage: str):
        return self.FORMATS.get(level).format(record=mesage)
    
    def formatTime(self, record, datefmt=LOG_DATE_FORMAT):
        # 获取当前时间并设置为东八区时间
        dt = datetime.fromtimestamp(record.created, pytz.timezone('Asia/Shanghai'))
        return dt.strftime(LOG_DATE_FORMAT)
    
    def format(self, record):
        record.message = record.getMessage()
        record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        record.asctime = self.formatTime(record, self.datefmt)
        log_category = CATEGORY_DEFAULT
        if isinstance(record.msg, ApiRequest):
            record.message = record.msg.to_dict()
            log_category = CATEGORY_API_REQUEST
        elif isinstance(record.msg, GlobalInterfaceMonitor):
            record.message = record.msg.to_dict()
            log_category = CATEGORY_GLOBAL_INTERFACE_MONITOR
        elif isinstance(record.msg, dict):
            record.message = record.msg
            log_category = CATEGORY_GLOBAL_INTERFACE_MONITOR
        log_json = {
            "time"     : f"{record.asctime}",
            "category" : log_category,
            "level"    : f"{record.levelname}",
            "msg"      : record.message,
            'host_name': get_host_name(),
            'business' : f'xguide-{env.Instance().get_env()}',
            "file"     : f"{record.filename}:{record.lineno}"
        }
        message = json.dumps(log_json, ensure_ascii=False)
        if env.Instance().is_debug():
            return self.format_with_color(record.levelno, message)
        
        return message
