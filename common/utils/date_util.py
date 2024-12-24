import calendar
import time
from datetime import datetime, timedelta

import pytz
from dateutil import parser
from dateutil.relativedelta import relativedelta

TIMEZONE_SHAGNHAI = 'Asia/Shanghai'

datefmt = "%Y-%m-%d %H:%M:%S"
datefmt_1 = '%Y%m%d%H%M%S'
# http RFC261的日期
datefmtRFC2616 = '%a, %d %b %Y %H:%M:%S GMT'


def timestamp_to_date(timestamp, format="%Y-%m-%d %H:%M:%S"):
    """
    将时间戳转换为日期格式的字符串。

    参数：
    - timestamp (int/float): 需要转换的时间戳。
    - format (str): 输出日期格式，默认值为"%Y-%m-%d %H:%M:%S"。

    返回：
    - str: 转换后的日期字符串。
    """
    return datetime.fromtimestamp(timestamp, get_timezone()).strftime(format)


def date_format(format: str = '%Y%m%d'):
    # 获取东八区时间 (北京时间)
    beijing_tz = pytz.timezone('Asia/Shanghai')
    current_time = datetime.now(beijing_tz)
    # 格式化为 '%Y%m%d' 格式
    return current_time.strftime(format)


def get_now_second():
    return int(time.time())


def get_now_mssecond():
    return int(time.time() * 1000)


def get_timezone():
    return pytz.timezone(TIMEZONE_SHAGNHAI)


def get_now_date_str(formatter=datefmt) -> str:
    return date_format(formatter)


# 获取基于当前时间 间隔多少天的日期时间
def get_delt_date_str(formatter: str = datefmt, hours: int = 0) -> str:
    return (datetime.now() + timedelta(hours=hours)).strftime(formatter)
    # return (datetime.now() +  timedelta(seconds=hours)).strftime(formatter)


# 获取RFC2616日期
def get_RFC2616_date_str(formatter: str = datefmtRFC2616) -> str:
    return datetime.utcnow().strftime(formatter)


def get_recommend_date(s):
    now = datetime.now()
    if not s:
        date_list = [now, now + timedelta(days=1), now + timedelta(days=2)]
    else:
        date_list = parse_date(now, s)
    if not date_list:
        date_list = [now, now + timedelta(days=1), now + timedelta(days=2)]
    ret_list = []
    for date in date_list:
        format_date = date.strftime('%Y-%m-%d')
        ret_list.append(format_date)
    
    return ret_list


def get_date_list(s):
    now = datetime.now()
    if not s:
        date_list = [now, now + timedelta(days=1), now + timedelta(days=2)]
    else:
        date_list = parse_date(now, s)
    return date_list


def parse_date(now: datetime, s: str) -> [datetime]:
    s = s.lower()
    # pattern = r'(20[2-9][0-9]|21[0-9][0-9])-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])'
    # if re.match(pattern, s):
    #     return [s]
    # 当前日期时间
    if s == '最近':
        return [now, now + timedelta(days=1), now + timedelta(days=2)]
    if s == '下周':
        next_week = now + timedelta(days=7 + 0 - now.weekday())
        return [next_week, next_week + timedelta(days=1), next_week + timedelta(days=2)]
    # 当前日期时间
    if s == '今天' or s == '现在' or s == '此刻' or s == '当前' or s == '这会' or s == '目前':
        return [now]
    # 昨天
    if s == '昨天' or s == 'yesterday':
        return [now - timedelta(days=1)]
    
    # 前天
    if s == '前天':
        return [now - timedelta(days=2)]
    
    # 明天
    if s == '明天' or s == 'tomorrow':
        return [now + timedelta(days=1)]
    
    # 后天
    if s == '后天' or s == 'the day after tomorrow':
        return [now + timedelta(days=2)]
        
        # 后天
    if s == '大后天':
        return [now + timedelta(days=3)]
    
    # 本周几
    if s in ['周一', '周二', '周三', '周四', '周五', '周六', '周日']:
        wd = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'].index(s)
        return [now + timedelta(days=wd - now.weekday())]
    
    # 下周几
    if s in ['下周一', '下周二', '下周三', '下周四', '下周五', '下周六', '下周日']:
        wd = ['下周一', '下周二', '下周三', '下周四', '下周五', '下周六', '下周日'].index(s)
        return [now + timedelta(days=7 + wd - now.weekday())]
    
    # 上周几
    if s in ['上周一', '上周二', '上周三', '上周四', '上周五', '上周六', '上周日']:
        wd = ['上周一', '上周二', '上周三', '上周四', '上周五', '上周六', '上周日'].index(s)
        return [now - timedelta(days=7 + now.weekday() - wd)]
    
    # 本月
    if s == '本月' or s == '本个月' or s == '这个月' or s == '这月' or s == '当月':
        return [now.replace(day=1)]
    
    # 下月
    if s == '下月' or s == '下个月':
        return [now.replace(day=1) + relativedelta(months=+1)]
    
    # 上月
    if s == '上月' or s == '上个月':
        return [now.replace(day=1) - relativedelta(months=1)]
    # 其他情况，使用dateutil库解析日期
    try:
        dt = [parser.parse(s).date()]
    except ValueError:
        dt = None
    return dt


def get_now_gpt_date_str():
    # 获取当前日期和时间
    now = datetime.now()
    
    # 获取今天的日期
    today_date = now.date()
    
    # 获取今天是星期几
    weekday = now.weekday()
    
    # 将星期几转换为中文
    weekday_chinese = calendar.day_name[weekday]
    
    # 替换英文星期名称为中文名称
    weekday_chinese = weekday_chinese.replace('Monday', '星期一') \
        .replace('Tuesday', '星期二') \
        .replace('Wednesday', '星期三') \
        .replace('Thursday', '星期四') \
        .replace('Friday', '星期五') \
        .replace('Saturday', '星期六') \
        .replace('Sunday', '星期日')
    
    # 格式化日期为 "xxxx年x月x日"
    formatted_date = today_date.strftime("%Y年-%m月-%d日")
    
    # 结果
    return f"今天是{formatted_date}，{weekday_chinese}"
