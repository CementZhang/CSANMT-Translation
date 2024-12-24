# _*_ coding: utf-8 _*_
import http
import logging
import logging.handlers as log_handlers
import time
import traceback

import httpx
import requests

from common.base.meta_singeton import MetaSingleton
from common.env import env
from common.utils.common import get_host_name
from common.utils.date_util import date_format
from common.utils.str_utils import get_work_dir
from . import logger_formatter

root_dir = get_work_dir()
DEFAULT_PATH = '/logs/'


class Logger(metaclass=MetaSingleton):
    def __init__(self):
        """
            指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        """
        # 屏蔽apscheduler DEBUG,INFO日志
        logging.getLogger('apscheduler').setLevel(logging.ERROR)
        
        hostname = get_host_name()
        # 创建一个logger
        self.logger = logging.getLogger(hostname)
        self.logger.setLevel(logging.INFO)
        
        # 创建一个handler，用于写入日志文件
        df = date_format()
        log_path = root_dir + DEFAULT_PATH
        log_name = f'{log_path}{df}_{hostname}.log'
        tengyun_formatter = logger_formatter.LogFormatter()
        # 基于100MB进行日志分片
        fh = log_handlers.RotatingFileHandler(log_name, maxBytes=1024 * 1024 * 100, backupCount=10)
        fh.setLevel(logging.INFO)
        fh.setFormatter(tengyun_formatter)
        self.logger.addHandler(fh)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(tengyun_formatter)
        self.logger.addHandler(ch)
    
    def get_log(self):
        return self.logger


def getlogger():
    return Logger().get_log()


def log_request_ensure_ascii_no(rsp: requests.Response, start_time: time.time):
    log_api_response(rsp, start_time)
    return


def log_api_request(url: str, header: dict, params: dict, context: dict = {}):
    """
    日志记录api请求
    """
    getlogger().info({'msg'    : 'log_api_request',
                      'traceid': context.get('traceid'), 'url': url, 'header': header, 'body': params})


def log_api_response(rsp: requests.Response, start_time: time.time, context: dict = {}, e: Exception = None,
                     stream: bool = False, decode_content=True):
    """
    日志记录api的响应，包含包括响应的内容、状态码、请求的 URL、耗时等
    """
    try:
        if not rsp:
            log_exception('request_error', e)
            return
        result = (
            rsp.content.decode() if decode_content and isinstance(rsp.content, bytes) else '') if not stream else ''
        url = rsp_url_format(rsp)
        body = None
        if isinstance(rsp, httpx.Response):
            body = rsp.request.content.decode('utf-8')
            body = body[:1024]
            result = rsp and rsp.content[:1024]
            if isinstance(result, bytes):
                result = result.decode('utf-8', errors='ignore')
        api_request = logger_formatter.ApiRequest(
                traceid=context.get('traceid'),
                url=url,
                header=rsp.request.headers,
                body=body,
                method=rsp.request.method,
                result=result,
                result_status=rsp.status_code,
                cost_time=int((time.time() - start_time) * 1000),
        )
        if not e or (rsp.status_code and rsp.status_code == http.HTTPStatus.OK.value):
            getlogger().info(api_request)
        else:
            api_request.error = str(e)
            getlogger().error(api_request)
        return
    except Exception as e:
        log_exception('', e)


def rsp_url_format(rsp):
    if isinstance(rsp, httpx.Response):
        url = str(rsp.url)
    elif isinstance(rsp, requests.Response):
        url = rsp.url
    else:
        url = ''
    return url


def log_exception(category: str, e: Exception, context: dict = {}):
    if not e:
        return
    
    if env.Instance().is_debug():
        traceback.print_exc()
    
    msg = str(e)
    # 打印异常堆栈信息
    e_traceback = traceback.format_exc()
    getlogger().error({"category": category, "traceid": context.get('traceid'), "msg": f"{msg}\n{e_traceback}"},
                      exc_info=True)
    return
